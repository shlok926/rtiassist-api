/**
 * RTI Assist - My RTIs Tracker Feature
 * Handles localStorage management, CRUD operations, UI updates
 * Author: RTI Assist Team
 * Date: 2026-03-03
 */

// ============================================
// 1️⃣ DATA MANAGEMENT (localStorage)
// ============================================

/**
 * RTI Data Schema
 * {
 *   id: "RTI_UNIQUE_ID_TIMESTAMP",
 *   description: "User's problem description",
 *   department: "Identified department",
 *   ministry: "Parent ministry",
 *   state: "State name or 'Central'",
 *   filedDate: "2026-03-03",
 *   referenceNumber: "User's RTI reference number",
 *   postNumber: "Registered post tracking number",
 *   status: "filed|pending|received|closed|rejected",
 *   quality_score: 88,
 *   draft: "Full RTI draft text",
 *   notes: "User's internal notes",
 *   dueDate: "2026-04-02", (30 days from filed)
 *   responses: [] (array of PIO responses)
 * }
 */

class RTITracker {
  constructor() {
    this.storageKey = 'rti_applications';
    this.initStorage();
  }

  // Initialize localStorage if empty
  initStorage() {
    if (!localStorage.getItem(this.storageKey)) {
      localStorage.setItem(this.storageKey, JSON.stringify([]));
    }
  }

  // ✅ CREATE - Add new RTI
  addRTI(rtiData) {
    try {
      const rtis = this.getAllRTIs();
      const newRTI = {
        id: 'RTI_' + Date.now(),
        description: rtiData.description,
        department: rtiData.department || 'Unknown',
        ministry: rtiData.ministry || 'Unknown',
        state: rtiData.state || 'Central',
        filedDate: new Date().toISOString().split('T')[0],
        referenceNumber: rtiData.referenceNumber || '',
        postNumber: rtiData.postNumber || '',
        status: 'filed',
        quality_score: rtiData.quality_score || 0,
        draft: rtiData.draft || '',
        notes: '',
        dueDate: this.calculateDueDate(),
        responses: [],
        createdAt: new Date().toISOString()
      };

      rtis.push(newRTI);
      localStorage.setItem(this.storageKey, JSON.stringify(rtis));
      console.log('✅ RTI Added:', newRTI.id);
      return newRTI;
    } catch (error) {
      console.error('❌ Error adding RTI:', error);
      return null;
    }
  }

  // ✅ READ - Get all RTIs
  getAllRTIs() {
    try {
      const data = localStorage.getItem(this.storageKey);
      return data ? JSON.parse(data) : [];
    } catch (error) {
      console.error('❌ Error reading RTIs:', error);
      return [];
    }
  }

  // ✅ READ - Get single RTI by ID
  getRTIById(id) {
    const rtis = this.getAllRTIs();
    return rtis.find(rti => rti.id === id) || null;
  }

  // ✅ READ - Get RTIs by status
  getRTIsByStatus(status) {
    const rtis = this.getAllRTIs();
    return rtis.filter(rti => rti.status === status);
  }

  // ✅ READ - Search RTIs
  searchRTIs(query) {
    const rtis = this.getAllRTIs();
    return rtis.filter(rti =>
      rti.description.toLowerCase().includes(query.toLowerCase()) ||
      rti.referenceNumber.toLowerCase().includes(query.toLowerCase()) ||
      rti.department.toLowerCase().includes(query.toLowerCase())
    );
  }

  // ✅ UPDATE - Update RTI status
  updateStatus(id, newStatus) {
    try {
      const rtis = this.getAllRTIs();
      const rti = rtis.find(r => r.id === id);
      if (rti) {
        rti.status = newStatus;
        rti.lastUpdated = new Date().toISOString();
        localStorage.setItem(this.storageKey, JSON.stringify(rtis));
        console.log('✅ Status Updated:', id, newStatus);
        return rti;
      }
      return null;
    } catch (error) {
      console.error('❌ Error updating status:', error);
      return null;
    }
  }

  // ✅ UPDATE - Add reference number
  updateReferenceNumber(id, refNumber) {
    try {
      const rtis = this.getAllRTIs();
      const rti = rtis.find(r => r.id === id);
      if (rti) {
        rti.referenceNumber = refNumber;
        localStorage.setItem(this.storageKey, JSON.stringify(rtis));
        return rti;
      }
      return null;
    } catch (error) {
      console.error('❌ Error updating reference:', error);
      return null;
    }
  }

  // ✅ UPDATE - Add post number
  updatePostNumber(id, postNumber) {
    try {
      const rtis = this.getAllRTIs();
      const rti = rtis.find(r => r.id === id);
      if (rti) {
        rti.postNumber = postNumber;
        localStorage.setItem(this.storageKey, JSON.stringify(rtis));
        return rti;
      }
      return null;
    } catch (error) {
      console.error('❌ Error updating post number:', error);
      return null;
    }
  }

  // ✅ UPDATE - Add notes
  updateNotes(id, notes) {
    try {
      const rtis = this.getAllRTIs();
      const rti = rtis.find(r => r.id === id);
      if (rti) {
        rti.notes = notes;
        localStorage.setItem(this.storageKey, JSON.stringify(rtis));
        return rti;
      }
      return null;
    } catch (error) {
      console.error('❌ Error updating notes:', error);
      return null;
    }
  }

  // ✅ UPDATE - Add PIO response
  addResponse(id, responseText) {
    try {
      const rtis = this.getAllRTIs();
      const rti = rtis.find(r => r.id === id);
      if (rti) {
        rti.responses.push({
          text: responseText,
          receivedDate: new Date().toISOString().split('T')[0],
          timestamp: new Date().toISOString()
        });
        rti.status = 'received';
        localStorage.setItem(this.storageKey, JSON.stringify(rtis));
        return rti;
      }
      return null;
    } catch (error) {
      console.error('❌ Error adding response:', error);
      return null;
    }
  }

  // ✅ DELETE - Remove RTI
  deleteRTI(id) {
    try {
      let rtis = this.getAllRTIs();
      rtis = rtis.filter(rti => rti.id !== id);
      localStorage.setItem(this.storageKey, JSON.stringify(rtis));
      console.log('✅ RTI Deleted:', id);
      return true;
    } catch (error) {
      console.error('❌ Error deleting RTI:', error);
      return false;
    }
  }

  // ============================================
  // 2️⃣ UTILITY FUNCTIONS
  // ============================================

  // Calculate due date (30 days from today)
  calculateDueDate() {
    const today = new Date();
    const dueDate = new Date(today.getTime() + 30 * 24 * 60 * 60 * 1000);
    return dueDate.toISOString().split('T')[0];
  }

  // Get days remaining until due date
  getDaysRemaining(dueDate) {
    const due = new Date(dueDate);
    const today = new Date();
    const diff = Math.ceil((due - today) / (1000 * 60 * 60 * 24));
    return diff > 0 ? diff : 0;
  }

  // Check if due date has passed
  isOverdue(dueDate) {
    const due = new Date(dueDate);
    const today = new Date();
    return today > due;
  }

  // Get status color
  getStatusColor(status) {
    const colors = {
      filed: '#FF6B00',      // Saffron
      pending: '#D4A017',    // Gold
      received: '#00A86B',   // Green
      closed: '#0A1628',     // Navy
      rejected: '#FF4444'    // Red
    };
    return colors[status] || '#8892A4';
  }

  // Get status emoji
  getStatusEmoji(status) {
    const emojis = {
      filed: '📝',
      pending: '⏳',
      received: '✅',
      closed: '🔒',
      rejected: '❌'
    };
    return emojis[status] || '❓';
  }

  // Export RTIs as CSV
  exportAsCSV() {
    try {
      const rtis = this.getAllRTIs();
      let csv = 'ID,Description,Department,State,Filed Date,Status,Reference Number,Due Date\n';
      
      rtis.forEach(rti => {
        csv += `"${rti.id}","${rti.description}","${rti.department}","${rti.state}","${rti.filedDate}","${rti.status}","${rti.referenceNumber}","${rti.dueDate}"\n`;
      });

      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `RTI_Applications_${new Date().toISOString().split('T')[0]}.csv`;
      link.click();
      console.log('✅ CSV Exported');
    } catch (error) {
      console.error('❌ Error exporting CSV:', error);
    }
  }

  // Get statistics
  getStatistics() {
    const rtis = this.getAllRTIs();
    return {
      total: rtis.length,
      filed: rtis.filter(r => r.status === 'filed').length,
      pending: rtis.filter(r => r.status === 'pending').length,
      received: rtis.filter(r => r.status === 'received').length,
      closed: rtis.filter(r => r.status === 'closed').length,
      rejected: rtis.filter(r => r.status === 'rejected').length,
      overdue: rtis.filter(r => this.isOverdue(r.dueDate)).length
    };
  }

  // Clear all RTIs (WARNING: Permanent!)
  clearAllRTIs() {
    if (confirm('⚠️ Are you sure? This will delete ALL RTI applications!')) {
      localStorage.setItem(this.storageKey, JSON.stringify([]));
      console.log('⚠️ All RTIs cleared');
      return true;
    }
    return false;
  }
}

// ============================================
// 3️⃣ UI FUNCTIONS
// ============================================

// Initialize tracker globally
const tracker = new RTITracker();

// Display all RTIs in the UI
function displayRTIs(filterStatus = null) {
  try {
    const rtis = filterStatus ? tracker.getRTIsByStatus(filterStatus) : tracker.getAllRTIs();
    const container = document.getElementById('rtisList');

    if (!container) {
      console.error('❌ #rtisList container not found');
      return;
    }

    if (rtis.length === 0) {
      container.innerHTML = `
        <div style="text-align:center;padding:2rem;color:var(--muted);">
          <p style="font-size:1.1rem;margin-bottom:1rem;">📭 No RTI applications yet</p>
          <p>Generate an RTI in the "Generate" tab to get started!</p>
        </div>
      `;
      return;
    }

    container.innerHTML = rtis.map(rti => `
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,107,0,0.1);border-radius:12px;padding:1.5rem;margin-bottom:1rem;cursor:pointer;" onclick="viewRTIDetails('${rti.id}')">
        <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.75rem;">
          <div>
            <h3 style="color:var(--saffron);margin:0;font-size:0.95rem;margin-bottom:0.25rem;">${rti.department}</h3>
            <p style="color:var(--muted);margin:0;font-size:0.8rem;">${rti.description.substring(0, 80)}...</p>
          </div>
          <div style="text-align:right;">
            <span style="display:inline-block;background:${tracker.getStatusColor(rti.status)};color:white;padding:0.25rem 0.75rem;border-radius:20px;font-size:0.7rem;font-weight:600;">${tracker.getStatusEmoji(rti.status)} ${rti.status.toUpperCase()}</span>
          </div>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:1rem;font-size:0.8rem;color:var(--muted);">
          <div><strong>Filed:</strong> ${rti.filedDate}</div>
          <div><strong>Due:</strong> ${rti.dueDate}</div>
          <div><strong>Reference:</strong> ${rti.referenceNumber || '—'}</div>
        </div>
        ${tracker.isOverdue(rti.dueDate) && rti.status === 'filed' ? `
          <div style="margin-top:0.75rem;padding:0.5rem;background:rgba(255,68,68,0.1);border-left:3px solid #FF4444;color:#FF8080;font-size:0.75rem;font-weight:600;">
            ⚠️ OVERDUE: No response from PIO
          </div>
        ` : ''}
      </div>
    `).join('');

    updateStatistics();
  } catch (error) {
    console.error('❌ Error displaying RTIs:', error);
  }
}

// View RTI details in modal
function viewRTIDetails(id) {
  try {
    const rti = tracker.getRTIById(id);
    if (!rti) {
      console.error('❌ RTI not found:', id);
      return;
    }

    const modal = document.getElementById('rtiDetailsModal');
    if (!modal) {
      console.error('❌ Modal not found');
      return;
    }

    const daysRemaining = tracker.getDaysRemaining(rti.dueDate);

    modal.innerHTML = `
      <div style="position:fixed;inset:0;background:rgba(0,0,0,0.7);display:flex;align-items:center;justify-content:center;z-index:1000;">
        <div style="background:var(--navy-mid);border:1px solid rgba(255,107,0,0.2);border-radius:16px;padding:2rem;max-width:600px;width:90%;max-height:90vh;overflow-y:auto;">
          
          <!-- Header -->
          <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:1.5rem;border-bottom:1px solid rgba(255,255,255,0.1);padding-bottom:1rem;">
            <div>
              <h2 style="color:var(--saffron);margin:0;font-size:1.2rem;">${rti.department}</h2>
              <p style="color:var(--muted);margin:0.5rem 0 0 0;font-size:0.8rem;">${rti.state}</p>
            </div>
            <button onclick="this.closest('div').parentElement.parentElement.style.display='none'" style="background:transparent;border:none;color:var(--muted);font-size:1.5rem;cursor:pointer;">✕</button>
          </div>

          <!-- Stats -->
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.5rem;">
            <div style="background:rgba(0,107,63,0.1);padding:1rem;border-radius:8px;">
              <div style="color:var(--muted);font-size:0.75rem;font-weight:600;">📅 FILED DATE</div>
              <div style="color:var(--green-light);font-size:1rem;font-weight:600;margin-top:0.25rem;">${rti.filedDate}</div>
            </div>
            <div style="background:${daysRemaining <= 5 ? 'rgba(255,68,68,0.1)' : 'rgba(212,160,23,0.1)'};padding:1rem;border-radius:8px;">
              <div style="color:var(--muted);font-size:0.75rem;font-weight:600;">⏳ DAYS REMAINING</div>
              <div style="color:${daysRemaining <= 5 ? '#FF8080' : 'var(--gold)'};font-size:1rem;font-weight:600;margin-top:0.25rem;">${daysRemaining}</div>
            </div>
          </div>

          <!-- Description -->
          <div style="margin-bottom:1.5rem;">
            <h3 style="color:var(--muted);font-size:0.75rem;font-weight:600;text-transform:uppercase;margin:0 0 0.5rem 0;">Your Problem</h3>
            <p style="background:rgba(255,255,255,0.02);padding:1rem;border-radius:8px;color:rgba(255,255,255,0.8);font-size:0.9rem;margin:0;line-height:1.6;">${rti.description}</p>
          </div>

          <!-- Reference Number -->
          <div style="margin-bottom:1.5rem;">
            <h3 style="color:var(--muted);font-size:0.75rem;font-weight:600;text-transform:uppercase;margin:0 0 0.5rem 0;">Reference Number</h3>
            <input type="text" placeholder="Enter RTI reference number from PIO" value="${rti.referenceNumber}" onchange="tracker.updateReferenceNumber('${id}', this.value); displayRTIs();" style="width:100%;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:0.75rem;color:white;font-family:monospace;font-size:0.9rem;" />
          </div>

          <!-- Post Number -->
          <div style="margin-bottom:1.5rem;">
            <h3 style="color:var(--muted);font-size:0.75rem;font-weight:600;text-transform:uppercase;margin:0 0 0.5rem 0;">Registered Post Number</h3>
            <input type="text" placeholder="Tracking number from postal service" value="${rti.postNumber}" onchange="tracker.updatePostNumber('${id}', this.value); displayRTIs();" style="width:100%;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:0.75rem;color:white;font-family:monospace;font-size:0.9rem;" />
          </div>

          <!-- Status -->
          <div style="margin-bottom:1.5rem;">
            <h3 style="color:var(--muted);font-size:0.75rem;font-weight:600;text-transform:uppercase;margin:0 0 0.5rem 0;">Status</h3>
            <select onchange="tracker.updateStatus('${id}', this.value); displayRTIs();" style="width:100%;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:0.75rem;color:white;font-size:0.9rem;">
              <option value="filed" ${rti.status === 'filed' ? 'selected' : ''}>📝 Filed</option>
              <option value="pending" ${rti.status === 'pending' ? 'selected' : ''}>⏳ Pending</option>
              <option value="received" ${rti.status === 'received' ? 'selected' : ''}>✅ Received</option>
              <option value="closed" ${rti.status === 'closed' ? 'selected' : ''}>🔒 Closed</option>
              <option value="rejected" ${rti.status === 'rejected' ? 'selected' : ''}>❌ Rejected</option>
            </select>
          </div>

          <!-- Notes -->
          <div style="margin-bottom:1.5rem;">
            <h3 style="color:var(--muted);font-size:0.75rem;font-weight:600;text-transform:uppercase;margin:0 0 0.5rem 0;">Notes</h3>
            <textarea placeholder="Add your notes..." value="${rti.notes}" onchange="tracker.updateNotes('${id}', this.value);" style="width:100%;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:8px;padding:0.75rem;color:white;font-family:'DM Sans',sans-serif;font-size:0.9rem;min-height:80px;"></textarea>
          </div>

          <!-- Actions -->
          <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:0.75rem;">
            <button onclick="copyToClipboard('${rti.draft}'); alert('✅ Draft copied!')" style="background:rgba(0,107,63,0.2);border:1px solid rgba(0,107,63,0.4);color:var(--green-light);padding:0.75rem;border-radius:8px;cursor:pointer;font-weight:600;font-size:0.8rem;">📋 Copy Draft</button>
            <button onclick="exportRTI('${id}')" style="background:rgba(212,160,23,0.2);border:1px solid rgba(212,160,23,0.4);color:var(--gold);padding:0.75rem;border-radius:8px;cursor:pointer;font-weight:600;font-size:0.8rem;">⬇️ Export</button>
            <button onclick="deleteRTIModal('${id}')" style="background:rgba(255,68,68,0.2);border:1px solid rgba(255,68,68,0.4);color:#FF8080;padding:0.75rem;border-radius:8px;cursor:pointer;font-weight:600;font-size:0.8rem;">🗑️ Delete</button>
          </div>

        </div>
      </div>
    `;
  } catch (error) {
    console.error('❌ Error viewing details:', error);
  }
}

// Close modal
function closeModal() {
  const modal = document.getElementById('rtiDetailsModal');
  if (modal) modal.innerHTML = '';
}

// Delete RTI with confirmation
function deleteRTIModal(id) {
  if (confirm('⚠️ Are you sure you want to delete this RTI application?')) {
    tracker.deleteRTI(id);
    displayRTIs();
    closeModal();
    alert('✅ RTI deleted successfully');
  }
}

// Export single RTI
function exportRTI(id) {
  try {
    const rti = tracker.getRTIById(id);
    if (!rti) return;

    const text = `RTI APPLICATION EXPORT\n${'='.repeat(50)}\n\nDepartment: ${rti.department}\nState: ${rti.state}\nStatus: ${rti.status}\nFiled Date: ${rti.filedDate}\nDue Date: ${rti.dueDate}\nReference: ${rti.referenceNumber || 'N/A'}\n\nDescription:\n${rti.description}\n\nDraft:\n${rti.draft}\n\nNotes:\n${rti.notes}`;

    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `RTI_${rti.id}.txt`;
    link.click();
  } catch (error) {
    console.error('❌ Error exporting:', error);
  }
}

// Copy to clipboard
function copyToClipboard(text) {
  navigator.clipboard.writeText(text);
}

// Filter RTIs by status
function filterByStatus(status) {
  displayRTIs(status === 'all' ? null : status);
}

// Search RTIs
function searchRTIs() {
  const query = document.getElementById('rtiSearchInput')?.value || '';
  if (!query) {
    displayRTIs();
    return;
  }

  try {
    const results = tracker.searchRTIs(query);
    const container = document.getElementById('rtisList');
    if (!container) return;

    if (results.length === 0) {
      container.innerHTML = `<p style="text-align:center;color:var(--muted);">No results found for "${query}"</p>`;
      return;
    }

    container.innerHTML = results.map(rti => `
      <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,107,0,0.1);border-radius:12px;padding:1.5rem;margin-bottom:1rem;cursor:pointer;" onclick="viewRTIDetails('${rti.id}')">
        <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:0.75rem;">
          <div>
            <h3 style="color:var(--saffron);margin:0;font-size:0.95rem;margin-bottom:0.25rem;">${rti.department}</h3>
            <p style="color:var(--muted);margin:0;font-size:0.8rem;">${rti.description.substring(0, 80)}...</p>
          </div>
          <span style="display:inline-block;background:${tracker.getStatusColor(rti.status)};color:white;padding:0.25rem 0.75rem;border-radius:20px;font-size:0.7rem;font-weight:600;">${tracker.getStatusEmoji(rti.status)} ${rti.status.toUpperCase()}</span>
        </div>
      </div>
    `).join('');
  } catch (error) {
    console.error('❌ Error searching:', error);
  }
}

// Update statistics display
function updateStatistics() {
  try {
    const stats = tracker.getStatistics();
    const statsDiv = document.getElementById('rtiStatistics');
    
    if (!statsDiv) return;

    statsDiv.innerHTML = `
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:0.75rem;">
        <div style="background:rgba(255,107,0,0.1);padding:1rem;border-radius:12px;text-align:center;">
          <div style="color:var(--saffron);font-size:1.5rem;font-weight:700;">${stats.total}</div>
          <div style="color:var(--muted);font-size:0.75rem;margin-top:0.25rem;">Total</div>
        </div>
        <div style="background:rgba(212,160,23,0.1);padding:1rem;border-radius:12px;text-align:center;">
          <div style="color:var(--gold);font-size:1.5rem;font-weight:700;">${stats.filed}</div>
          <div style="color:var(--muted);font-size:0.75rem;margin-top:0.25rem;">Filed</div>
        </div>
        <div style="background:rgba(0,107,63,0.1);padding:1rem;border-radius:12px;text-align:center;">
          <div style="color:var(--green-light);font-size:1.5rem;font-weight:700;">${stats.received}</div>
          <div style="color:var(--muted);font-size:0.75rem;margin-top:0.25rem;">Received</div>
        </div>
        <div style="background:rgba(255,68,68,0.1);padding:1rem;border-radius:12px;text-align:center;">
          <div style="color:#FF8080;font-size:1.5rem;font-weight:700;">${stats.overdue}</div>
          <div style="color:var(--muted);font-size:0.75rem;margin-top:0.25rem;">Overdue</div>
        </div>
      </div>
    `;
  } catch (error) {
    console.error('❌ Error updating stats:', error);
  }
}

// Add RTI from generated application (call from main Generate function)
function addRTIFromGenerated(apiResponse) {
  try {
    const rti = tracker.addRTI({
      description: apiResponse.information_needed || 'Generated RTI',
      department: apiResponse.department,
      ministry: apiResponse.ministry,
      state: apiResponse.government_level === 'central' ? 'Central' : 'Unknown',
      quality_score: apiResponse.quality_score,
      draft: apiResponse.draft,
      referenceNumber: ''
    });

    if (rti) {
      console.log('✅ RTI added to tracker:', rti.id);
      return rti.id;
    }
  } catch (error) {
    console.error('❌ Error adding generated RTI:', error);
  }
}

// ============================================
// 4️⃣ INITIALIZATION
// ============================================

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  console.log('📊 RTI Tracker Initialized');
  displayRTIs();
});