import React, { useState, useEffect } from 'react';
import FirstAppealModal from '../rti/FirstAppealModal';
import { useAuth } from '../../context/AuthContext';
import { apiFetch } from '../../utils/api';

const Tracker = ({ setActiveTab, setSelectedCaseId }) => {
  const { user } = useAuth();
  const [rtis, setRtis] = useState([]);
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [isAppealModalOpen, setIsAppealModalOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (user) {
      loadCases();
    }
  }, [user]);

  const loadCases = async () => {
    setIsLoading(true);
    try {
      // 1. Migrate legacy data if exists
      const legacyData = localStorage.getItem('rti_tracker');
      if (legacyData) {
        try {
          const parsed = JSON.parse(legacyData);
          for (const item of parsed) {
            await apiFetch('/cases/import', {
              method: 'POST',
              body: JSON.stringify(item)
            });
          }
          localStorage.removeItem('rti_tracker');
        } catch (e) {
          console.error("Migration failed", e);
        }
      }

      // 2. Load from backend
      const res = await apiFetch('/cases');
      if (res.ok) {
        const data = await res.json();
        // Map backend cases to frontend tracker format
        const formatted = data.cases.map(c => ({
          id: c.id,
          date: c.filing_date || c.created_at,
          department: c.title || c.problem_description.substring(0, 50) + '...',
          description: c.problem_description,
          status: getFrontendStatus(c.status),
          backend_status: c.status,
          next_deadline: c.next_deadline,
          remaining_days: c.remaining_days,
          overdue: c.overdue
        }));
        setRtis(formatted);
      }
    } catch (e) {
      console.error("Failed to load cases", e);
    } finally {
      setIsLoading(false);
    }
  };

  const getFrontendStatus = (backendStatus) => {
    switch (backendStatus) {
      case 'READY_TO_FILE': return 'pending';
      case 'AWAITING_RESPONSE': return 'filed';
      case 'RESPONSE_RECEIVED':
      case 'ANALYSIS_READY': return 'received';
      case 'APPEAL_RECOMMENDED':
      case 'APPEAL_CONFIRMED':
      case 'APPEAL_FILED': return 'pending';
      default: return 'pending';
    }
  };

  const deleteRTI = async (id) => {
    // Delete API not strictly defined in Phase 2, omit or mock
    alert("Delete operation must be performed via case settings.");
  };

  const updateStatus = async (id, newStatus) => {
    alert("Status is managed automatically by the backend lifecycle.");
  };

  // Filter & Search Logic
  const filteredRTIs = rtis.filter(rti => {
    const matchesFilter = filter === 'all' || rti.status === filter;
    const matchesSearch = search === '' || 
      (rti.department && rti.department.toLowerCase().includes(search.toLowerCase())) ||
      (rti.description && rti.description.toLowerCase().includes(search.toLowerCase()));
    return matchesFilter && matchesSearch;
  });

  const getStatusColor = (status) => {
    switch(status) {
      case 'filed': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'received': return 'bg-green-100 text-green-800';
      case 'rejected': return 'bg-red-100 text-red-800';
      case 'closed': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="w-full max-w-5xl mx-auto p-4 md:p-8 animate-fade-in">
      {!user ? (
        <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center flex flex-col items-center justify-center">
          <div className="text-4xl mb-4">🔒</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Authentication Required</h2>
          <p className="text-gray-600 mb-6">Please log in to manage your RTI applications and track deadlines.</p>
        </div>
      ) : (
        <>
          <div className="mb-8">
        <h2 className="text-3xl font-black text-gray-900 mb-2">📋 My RTI Applications</h2>
        <p className="text-gray-600">Track all your filed RTIs. Search, filter, update status, and manage deadlines locally.</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 text-center">
          <div className="text-2xl font-bold text-gray-800">{rtis.length}</div>
          <div className="text-xs font-semibold text-gray-500 uppercase mt-1">Total RTIs</div>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 text-center">
          <div className="text-2xl font-bold text-yellow-600">{rtis.filter(r => r.status === 'pending' || r.status === 'filed').length}</div>
          <div className="text-xs font-semibold text-gray-500 uppercase mt-1">Active / Pending</div>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 text-center">
          <div className="text-2xl font-bold text-green-600">{rtis.filter(r => r.status === 'received').length}</div>
          <div className="text-xs font-semibold text-gray-500 uppercase mt-1">Received</div>
        </div>
        <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 text-center">
          <div className="text-2xl font-bold text-red-600">{rtis.filter(r => r.status === 'rejected').length}</div>
          <div className="text-xs font-semibold text-gray-500 uppercase mt-1">Rejected</div>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-6 flex flex-col md:flex-row gap-4">
        <input 
          type="text" 
          placeholder="🔍 Search by department, description..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rti-blue"
        />
        <div className="flex flex-wrap gap-2 items-center">
          {['all', 'filed', 'pending', 'received', 'rejected', 'closed'].map(f => (
            <button 
              key={f}
              onClick={() => setFilter(f)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium capitalize transition-colors border
                ${filter === f ? 'bg-gray-800 text-white border-gray-800' : 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'}`}
            >
              {f}
            </button>
          ))}
        </div>
      </div>

      {/* List */}
      <div className="space-y-4">
        {filteredRTIs.length === 0 ? (
          <div className="bg-white p-8 rounded-xl shadow-sm border border-gray-100 text-center text-gray-500">
            {search || filter !== 'all' ? "No RTIs match your filters." : "You haven't saved any RTIs to the tracker yet."}
          </div>
        ) : (
          filteredRTIs.map((rti) => {
            const isLate = rti.overdue;
            const daysLeft = rti.remaining_days !== null ? rti.remaining_days : 0;
            return (
              <div key={rti.id} className="bg-white p-5 rounded-xl shadow-sm border border-gray-100 flex flex-col md:flex-row gap-4 items-start md:items-center hover:shadow-md transition-shadow">
                
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-bold capitalize ${getStatusColor(rti.status)}`}>
                      {rti.status}
                    </span>
                    <span className="text-xs text-gray-400 font-mono">{new Date(rti.date).toLocaleDateString()}</span>
                  </div>
                  <h4 className="font-bold text-gray-800 mb-1">{rti.department}</h4>
                  <p className="text-sm text-gray-600 line-clamp-2">{rti.description}</p>
                </div>

                <div className="flex flex-col md:items-end gap-3 w-full md:w-auto mt-4 md:mt-0 border-t md:border-t-0 border-gray-100 pt-4 md:pt-0">
                  <div className="text-center md:text-right flex flex-col gap-2">
                    {rti.remaining_days !== null && (
                      <div className={`text-sm font-bold ${isLate ? 'text-red-600' : 'text-orange-500'}`}>
                        {isLate ? `⚠️ ${Math.abs(daysLeft)} Days Overdue` : `⏰ ${daysLeft} Days Left`}
                      </div>
                    )}
                    <button 
                      onClick={() => {
                        setSelectedCaseId(rti.id);
                        setActiveTab('case-detail');
                      }}
                      className="text-xs font-bold text-rti-blue bg-blue-50 hover:bg-blue-100 border border-blue-200 px-3 py-1 rounded transition-colors"
                    >
                      View Case
                    </button>
                    {rti.backend_status === 'ANALYSIS_READY' && (
                      <button 
                        onClick={() => setIsAppealModalOpen(true)}
                        className="text-xs font-bold text-red-600 bg-red-50 hover:bg-red-100 border border-red-200 px-2 py-1 rounded transition-colors"
                      >
                        📝 File Appeal
                      </button>
                    )}
                  </div>
                  
                  <div className="flex gap-2">
                    <button 
                      onClick={() => deleteRTI(rti.id)}
                      className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete"
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>

              </div>
            );
          })
        )}
      </div>

      <FirstAppealModal 
        isOpen={isAppealModalOpen} 
        onClose={() => setIsAppealModalOpen(false)} 
      />
        </>
      )}
    </div>
  );
};

export default Tracker;
