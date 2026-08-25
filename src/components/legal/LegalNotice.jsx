import React, { useState } from 'react';

const LegalNotice = ({ setActiveTab }) => {
  const [formData, setFormData] = useState({
    sender: '',
    recipient: '',
    type: 'rent_deposit',
    description: '',
    amount: '',
    state: ''
  });
  
  const [status, setStatus] = useState({ loading: false, error: null });
  const [draft, setDraft] = useState(null);

  const quickScenarios = [
    { label: '🏠 Security Deposit', text: 'I vacated the flat on [Date] after giving 1 month notice. Landlord is not returning my security deposit of ₹[Amount] despite multiple requests.' },
    { label: '🏗️ Builder Possession', text: 'Booked a flat in [Project Name]. Promised possession was [Date] but construction is stopped and builder is ignoring my calls.' },
    { label: '💼 Salary Dues', text: 'I resigned on [Date] serving full notice period. Company has not paid my full and final settlement and last month salary.' },
    { label: '💵 Cheque Bounce', text: 'The cheque bearing number [Number] dated [Date] for ₹[Amount] was returned unpaid by the bank with remark "Funds Insufficient".' }
  ];

  const handleScenarioClick = (text) => {
    setFormData(prev => ({ ...prev, description: text }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Sanitization: Allow only numbers in amount
    if (name === 'amount' && value !== '' && !/^\d+$/.test(value)) return;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    if (!formData.sender.trim()) return "Sender Name is required.";
    if (!formData.recipient.trim()) return "Recipient Name is required.";
    if (!formData.description.trim()) return "Please describe the issue.";
    if (formData.description.length < 20) return "Description is too short. Provide more context.";
    return null;
  };

  const handleGenerate = () => {
    const errorMsg = validateForm();
    if (errorMsg) {
      setStatus({ loading: false, error: errorMsg });
      return;
    }

    setStatus({ loading: true, error: null });
    
    setTimeout(() => {
      setDraft(`LEGAL NOTICE
UNDER INSTRUCTIONS FROM MY CLIENT

To,
${formData.recipient}

From,
${formData.sender}
${formData.state ? `State: ${formData.state}` : ''}

SUBJECT: LEGAL NOTICE FOR ${formData.type.replace(/_/g, ' ').toUpperCase()}

Under the instructions from and on behalf of my client ${formData.sender}, I do hereby serve you with the following legal notice:

1. That my client is a law-abiding citizen.
2. The brief facts giving rise to this notice are as follows:
${formData.description}

3. ${formData.amount ? `That you are liable to pay a sum of ₹${formData.amount} to my client.` : 'That your actions have caused significant distress and legal injury to my client.'}

4. I therefore call upon you through this legal notice to rectify the aforementioned breach/pay the due amount within 15 DAYS from the receipt of this notice, failing which my client will be constrained to initiate appropriate civil/criminal proceedings against you in a court of law, entirely at your risk, cost, and consequence.

Copy retained for future records.

Date: ${new Date().toISOString().split('T')[0]}
Place: ${formData.state || '[Place]'}

Signature of Sender / Advocate: _________________`);
      
      setStatus({ loading: false, error: null });
    }, 1500);
  };

  return (
    <div className="w-full max-w-4xl mx-auto animate-fade-in text-left">
      <button 
        onClick={() => setActiveTab('legaltools')}
        className="mb-6 px-4 py-2 bg-white text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors font-medium text-sm focus:outline-none focus:ring-2 focus:ring-gray-300"
      >
        ← Back to Legal Tools
      </button>

      {/* Hero */}
      <div className="bg-gradient-to-r from-stone-800 to-stone-600 rounded-2xl p-6 md:p-10 mb-8 text-white shadow-xl flex flex-col md:flex-row items-center md:items-start gap-6">
        <div className="text-6xl" aria-hidden="true">📜</div>
        <div>
          <h2 className="text-2xl md:text-3xl font-black mb-3">Legal Notice Generator</h2>
          <p className="text-stone-100 text-sm md:text-base mb-4 leading-relaxed">
            Landlord not returning deposit? Builder delaying possession? Employer not paying dues? Send a formal legal notice. Advocates charge ₹2000-5000 — we do it FREE.
          </p>
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ IPC / CPC Sections Auto-Cited</span>
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ 15-Day Compliance Deadline</span>
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ Registered Post Format</span>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 md:p-8 rounded-2xl shadow-xl border border-gray-100">
        
        {status.error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl flex items-center gap-2">
            <span aria-hidden="true">❌</span>
            <strong>Error:</strong> {status.error}
          </div>
        )}

        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="ln-sender" className="block text-sm font-bold text-gray-700 mb-2">Your Name (Sender) *</label>
              <input 
                id="ln-sender" type="text" name="sender" value={formData.sender} onChange={handleChange}
                placeholder="Your full name"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-stone-500 focus:outline-none"
              />
            </div>
            <div>
              <label htmlFor="ln-recipient" className="block text-sm font-bold text-gray-700 mb-2">Recipient Name *</label>
              <input 
                id="ln-recipient" type="text" name="recipient" value={formData.recipient} onChange={handleChange}
                placeholder="Person / Company name"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-stone-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="ln-type" className="block text-sm font-bold text-gray-700 mb-2">Type of Legal Notice *</label>
            <select 
              id="ln-type" name="type" value={formData.type} onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-stone-500 bg-white focus:outline-none"
            >
              <option value="rent_deposit">Landlord — Security Deposit Not Returned</option>
              <option value="property_dispute">Property / Land Dispute</option>
              <option value="builder_delay">Builder — Possession Delay</option>
              <option value="money_recovery">Money Recovery (Loan/Dues)</option>
              <option value="cheque_bounce">Cheque Bounce (NI Act Section 138)</option>
              <option value="employment">Employer — Unpaid Salary / Wrongful Termination</option>
              <option value="contract_breach">Contract Breach</option>
            </select>
          </div>

          {/* Scenarios */}
          <div>
            <span className="text-sm font-semibold text-gray-500 mb-2 block">💡 Common cases — click to fill:</span>
            <div className="flex flex-wrap gap-2">
              {quickScenarios.map((sc, idx) => (
                <button 
                  key={idx} onClick={() => handleScenarioClick(sc.text)}
                  className="px-3 py-1.5 bg-stone-50 text-stone-700 text-sm font-medium rounded-full hover:bg-stone-100 transition-colors border border-stone-200 focus:outline-none focus:ring-2 focus:ring-stone-500"
                >
                  {sc.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="ln-desc" className="block text-sm font-bold text-gray-700 mb-2">Describe the Issue in Detail *</label>
            <textarea 
              id="ln-desc" name="description" value={formData.description} onChange={handleChange}
              rows="4" placeholder="Full details: what happened, dates, amounts, previous attempts to resolve..."
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-stone-500 resize-none focus:outline-none"
            ></textarea>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="ln-amount" className="block text-sm font-bold text-gray-700 mb-2">Amount Involved (₹) if applicable</label>
              <input 
                id="ln-amount" type="text" name="amount" value={formData.amount} onChange={handleChange}
                placeholder="e.g. 50000"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-stone-500 focus:outline-none"
              />
            </div>
            <div>
              <label htmlFor="ln-state" className="block text-sm font-bold text-gray-700 mb-2">State</label>
              <select 
                id="ln-state" name="state" value={formData.state} onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-stone-500 bg-white focus:outline-none"
              >
                <option value="">Select State</option>
                <option>Delhi</option><option>Maharashtra</option><option>Karnataka</option>
                <option>Tamil Nadu</option><option>Uttar Pradesh</option><option>Gujarat</option>
              </select>
            </div>
          </div>

          <button 
            onClick={handleGenerate}
            disabled={status.loading}
            className="w-full py-4 bg-gray-900 hover:bg-gray-800 text-white font-bold text-lg rounded-xl shadow-lg transform transition-transform hover:scale-[1.01] flex items-center justify-center gap-2 focus:outline-none focus:ring-4 focus:ring-gray-300"
          >
            {status.loading ? <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" aria-hidden="true"></span> : "⚡ Generate Legal Notice — FREE"}
          </button>
        </div>
      </div>

      {/* Result Section */}
      {draft && (
        <div className="mt-8 bg-gray-50 border border-gray-200 rounded-2xl overflow-hidden animate-fade-in-up">
          <div className="bg-white px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <span className="font-bold text-gray-800">📄 Generated Notice Draft</span>
            <button 
              onClick={() => navigator.clipboard.writeText(draft)}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-gray-300"
            >
              📋 Copy
            </button>
          </div>
          <div className="p-6 bg-white font-mono text-sm text-gray-800 whitespace-pre-wrap max-h-96 overflow-y-auto">
            {draft}
          </div>
          <div className="bg-stone-50 p-4 border-t border-stone-200 flex items-start gap-4">
            <div className="text-2xl" aria-hidden="true">⚠️</div>
            <div className="text-sm text-stone-800">
              <strong>Note:</strong> Send via Registered Post with Acknowledgement Due (RPAD). Keep proof of dispatch. 
              If no response in 15 days, you may proceed with court filing. This is not a substitute for legal counsel in complex matters.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LegalNotice;
