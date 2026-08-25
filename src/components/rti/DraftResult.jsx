import React, { useState } from 'react';
import FirstAppealModal from './FirstAppealModal';

const DraftResult = ({ data, onReset }) => {
  const [isAppealModalOpen, setIsAppealModalOpen] = useState(false);
  
  if (!data) return null;

  const handleSaveToTracker = () => {
    try {
      const existingStr = localStorage.getItem('rti_tracker');
      const existing = existingStr ? JSON.parse(existingStr) : [];
      
      const newRTI = {
        id: Date.now().toString(),
        department: data.department || 'Unknown Department',
        description: data.information_needed || 'RTI Application',
        date: new Date().toISOString(),
        status: 'filed',
        draft: data.draft,
        quality: data.quality_score
      };
      
      localStorage.setItem('rti_tracker', JSON.stringify([newRTI, ...existing]));
      alert('✅ Saved to My RTIs Tracker successfully!');
    } catch (e) {
      console.error(e);
      alert('Failed to save to tracker');
    }
  };

  return (
    <div className="mt-8 pt-8 border-t border-gray-100 animate-fade-in-up">
      {/* Header Info */}
      <div className="flex items-start justify-between mb-6 bg-green-50 border border-green-100 p-4 rounded-xl">
        <div>
          <h3 className="text-xl font-bold text-green-800 mb-2">✅ RTI Application Generated!</h3>
          <div className="text-sm text-green-700 leading-relaxed">
            Dept: <strong>{data.department}</strong> · Ministry: <strong>{data.ministry}</strong><br/>
            Urgency: <strong className="capitalize">{data.urgency}</strong> · Confidence: <strong>{Math.round(data.confidence * 100)}%</strong>
          </div>
        </div>
        <div className="text-3xl">🏛</div>
      </div>

      {/* Portal Link */}
      {data.pio_details?.online_portal && (
        <a 
          href={data.pio_details.online_portal} 
          target="_blank" 
          rel="noopener noreferrer"
          className="flex items-center justify-between p-4 mb-6 bg-blue-50 border border-blue-100 rounded-xl hover:bg-blue-100 transition-colors group"
        >
          <div className="flex items-center gap-3">
            <span className="text-2xl">🔗</span>
            <div>
              <div className="font-bold text-blue-900">File Online Now</div>
              <div className="text-sm text-blue-700">Official RTI filing portal</div>
            </div>
          </div>
          <span className="text-blue-500 group-hover:translate-x-1 transition-transform">→</span>
        </a>
      )}

      <button 
        onClick={handleSaveToTracker}
        className="w-full mb-6 py-3 bg-gray-100 hover:bg-gray-200 text-gray-800 font-bold rounded-xl transition-colors border border-gray-300"
      >
        📋 Save to My RTIs Tracker
      </button>

      {/* Scores Grid */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        <div className="bg-slate-50 p-4 rounded-xl border border-gray-100 text-center">
          <div className="text-2xl font-black text-rti-blue">{data.quality_score}/100</div>
          <div className="text-xs font-semibold text-gray-500 uppercase mt-1">Quality Score</div>
        </div>
        <div className="bg-slate-50 p-4 rounded-xl border border-gray-100 text-center">
          <div className="text-2xl font-black text-rti-green capitalize">{data.estimated_success_probability}</div>
          <div className="text-xs font-semibold text-gray-500 uppercase mt-1">Success Chance</div>
        </div>
        <div className="bg-slate-50 p-4 rounded-xl border border-gray-100 text-center">
          <div className="text-2xl font-black text-orange-500 capitalize">{data.exempt_risk}</div>
          <div className="text-xs font-semibold text-gray-500 uppercase mt-1">Exempt Risk</div>
        </div>
      </div>

      {/* Draft Box */}
      <div className="bg-gray-50 border border-gray-200 rounded-xl overflow-hidden mb-8">
        <div className="bg-gray-100 px-4 py-3 border-b border-gray-200 flex justify-between items-center">
          <span className="font-bold text-gray-700">📄 Your RTI Application Draft</span>
          <div className="flex gap-2">
            <button 
              onClick={() => navigator.clipboard.writeText(data.draft)}
              className="px-3 py-1.5 bg-white border border-gray-300 rounded text-sm font-medium hover:bg-gray-50"
            >
              📋 Copy
            </button>
          </div>
        </div>
        <div className="p-6 bg-white font-mono text-sm text-gray-800 whitespace-pre-wrap leading-relaxed max-h-96 overflow-y-auto">
          {data.draft}
        </div>
      </div>

      {/* Warnings & Suggestions */}
      {data.warnings && data.warnings.length > 0 && (
        <div className="mb-8 bg-yellow-50 border border-yellow-200 rounded-xl p-4">
          <div className="font-bold text-yellow-800 mb-2">⚠️ AI Suggestions</div>
          <ul className="list-disc pl-5 text-sm text-yellow-700 space-y-1">
            {data.warnings.map((w, i) => <li key={i}>{w}</li>)}
          </ul>
        </div>
      )}

      {/* Filing Instructions */}
      <div className="mb-8">
        <h4 className="font-bold text-gray-800 mb-3 text-lg">📋 How to File This RTI</h4>
        <div className="bg-blue-50 border border-blue-100 p-5 rounded-xl text-sm text-blue-900 whitespace-pre-wrap leading-relaxed">
          {data.filing_instructions}
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 mt-8">
        <button 
          onClick={() => setIsAppealModalOpen(true)}
          className="flex-1 py-3 bg-red-50 text-red-700 hover:bg-red-100 font-bold border border-red-200 rounded-xl transition-colors flex items-center justify-center gap-2"
        >
          📝 Generate First Appeal
        </button>
        <button 
          onClick={onReset}
          className="flex-1 py-3 bg-white hover:bg-gray-50 text-gray-700 font-bold border border-gray-300 rounded-xl transition-colors"
        >
          🔄 New Application
        </button>
      </div>

      <FirstAppealModal 
        isOpen={isAppealModalOpen} 
        onClose={() => setIsAppealModalOpen(false)} 
      />
    </div>
  );
};

export default DraftResult;
