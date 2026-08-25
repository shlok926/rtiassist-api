import React, { useState } from 'react';

const ConsumerCourt = ({ setActiveTab }) => {
  const [formData, setFormData] = useState({
    name: '',
    address: '',
    company: '',
    type: 'defective_product',
    description: '',
    amount: '',
    date: '',
    relief: 'refund'
  });
  
  const [status, setStatus] = useState({ loading: false, error: null });
  const [draft, setDraft] = useState(null);

  const quickScenarios = [
    { label: '🛒 Ecomm Refund', text: 'Ordered product online but received empty box/wrong item. Company refusing refund despite multiple complaints.' },
    { label: '🏦 Insurance Claim', text: 'Health insurance claim rejected citing pre-existing disease arbitrarily without medical evidence.' },
    { label: '🏠 Builder Delay', text: 'Booked flat in project. Possession delayed by 2 years beyond promised date. Builder not refunding money.' },
    { label: '📱 Defective Product', text: 'Purchased mobile phone which stopped working in 10 days. Service center refusing free repair under warranty.' }
  ];

  const handleScenarioClick = (text) => {
    setFormData(prev => ({ ...prev, description: text }));
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Basic sanitization for amount to only allow numbers
    if (name === 'amount' && value !== '' && !/^\d+$/.test(value)) {
      return; 
    }
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const validateForm = () => {
    if (!formData.name.trim()) return "Full Name is required.";
    if (!formData.address.trim()) return "Address is required.";
    if (!formData.company.trim()) return "Company / Opposite Party is required.";
    if (!formData.description.trim()) return "Please describe the problem in detail.";
    if (formData.description.length < 20) return "Description is too short. Please provide more details.";
    return null;
  };

  const handleGenerate = () => {
    const errorMsg = validateForm();
    if (errorMsg) {
      setStatus({ loading: false, error: errorMsg });
      return;
    }

    setStatus({ loading: true, error: null });
    
    // Simulate secure API call and draft generation
    setTimeout(() => {
      // Note: In production, this draft generation happens on the backend to prevent business logic exposure
      // For now, generating a mock string that safely escapes any HTML (handled naturally by React later)
      setDraft(`BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION
Complaint under Section 35 of the Consumer Protection Act, 2019

BETWEEN
COMPLAINANT:
${formData.name}
${formData.address}

AND
OPPOSITE PARTY:
${formData.company}

1. BRIEF FACTS:
The complainant purchased/availed services on ${formData.date || '[Date not provided]'}. 
The total amount involved in this transaction is ₹${formData.amount || '[Amount not specified]'}.

2. NATURE OF COMPLAINT: (${formData.type.replace(/_/g, ' ').toUpperCase()})
${formData.description}

3. RELIEF SOUGHT:
The complainant respectfully prays that the Hon'ble Commission may direct the Opposite Party to provide the following relief: 
${formData.relief.replace(/_/g, ' ').toUpperCase()}.

Verification:
Verified that the contents of this complaint are true to the best of my knowledge.

Date: ${new Date().toISOString().split('T')[0]}
Signature: _________________`);
      
      setStatus({ loading: false, error: null });
    }, 1500);
  };

  return (
    <div className="w-full max-w-4xl mx-auto animate-fade-in text-left">
      <button 
        onClick={() => setActiveTab('legaltools')}
        className="mb-6 px-4 py-2 bg-white text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors font-medium text-sm"
        aria-label="Back to Legal Tools Hub"
      >
        ← Back to Legal Tools
      </button>

      {/* Hero */}
      <div className="bg-gradient-to-r from-orange-800 to-orange-600 rounded-2xl p-6 md:p-10 mb-8 text-white shadow-xl flex flex-col md:flex-row items-center md:items-start gap-6">
        <div className="text-6xl" aria-hidden="true">🛒</div>
        <div>
          <h2 className="text-2xl md:text-3xl font-black mb-3">Consumer Court Complaint</h2>
          <p className="text-orange-100 text-sm md:text-base mb-4 leading-relaxed">
            Product defective? Service not delivered? Company refusing refund? File complaint to Consumer Disputes Redressal Forum under Consumer Protection Act 2019. No lawyer needed.
          </p>
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ Consumer Protection Act 2019</span>
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ EDAAKHIL Format</span>
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
              <label htmlFor="cc-name" className="block text-sm font-bold text-gray-700 mb-2">Your Full Name *</label>
              <input 
                id="cc-name" type="text" name="name" value={formData.name} onChange={handleChange}
                placeholder="Complainant name"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"
                required
              />
            </div>
            <div>
              <label htmlFor="cc-address" className="block text-sm font-bold text-gray-700 mb-2">Your Address *</label>
              <input 
                id="cc-address" type="text" name="address" value={formData.address} onChange={handleChange}
                placeholder="Full address with pin code"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="cc-company" className="block text-sm font-bold text-gray-700 mb-2">Company / Opposite Party *</label>
            <input 
              id="cc-company" type="text" name="company" value={formData.company} onChange={handleChange}
              placeholder="e.g. Amazon India, Flipkart, Builder XYZ, Hospital ABC"
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="cc-type" className="block text-sm font-bold text-gray-700 mb-2">Type of Complaint *</label>
            <select 
              id="cc-type" name="type" value={formData.type} onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 bg-white focus:outline-none"
            >
              <option value="defective_product">Defective Product</option>
              <option value="service_deficiency">Deficiency in Service</option>
              <option value="refund_denied">Refund/Return Denied</option>
              <option value="misleading_ad">Misleading Advertisement</option>
              <option value="overcharging">Overcharging / Unfair Trade Practice</option>
              <option value="builder_delay">Builder Delay / RERA Matter</option>
            </select>
          </div>

          {/* Scenarios */}
          <div>
            <span className="text-sm font-semibold text-gray-500 mb-2 block">💡 Common problems — click to fill:</span>
            <div className="flex flex-wrap gap-2">
              {quickScenarios.map((sc, idx) => (
                <button 
                  key={idx} onClick={() => handleScenarioClick(sc.text)}
                  className="px-3 py-1.5 bg-orange-50 text-orange-700 text-sm font-medium rounded-full hover:bg-orange-100 transition-colors border border-orange-100 focus:outline-none focus:ring-2 focus:ring-orange-500"
                >
                  {sc.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="cc-desc" className="block text-sm font-bold text-gray-700 mb-2">Describe the Problem in Detail *</label>
            <textarea 
              id="cc-desc" name="description" value={formData.description} onChange={handleChange}
              rows="4" placeholder="What happened? Order ID, dates, what the company did wrong..."
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 resize-none focus:outline-none"
              required
            ></textarea>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="cc-amount" className="block text-sm font-bold text-gray-700 mb-2">Amount Involved (₹)</label>
              <input 
                id="cc-amount" type="text" name="amount" value={formData.amount} onChange={handleChange}
                placeholder="e.g. 15000"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none"
              />
            </div>
            <div>
              <label htmlFor="cc-date" className="block text-sm font-bold text-gray-700 mb-2">Date of Purchase/Service</label>
              <input 
                id="cc-date" type="date" name="date" value={formData.date} onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 focus:outline-none text-gray-700"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="cc-relief" className="block text-sm font-bold text-gray-700 mb-2">Relief Sought</label>
            <select 
              id="cc-relief" name="relief" value={formData.relief} onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 bg-white focus:outline-none text-gray-700"
            >
              <option value="refund">Full Refund</option>
              <option value="replacement">Product Replacement</option>
              <option value="compensation">Compensation for Loss</option>
              <option value="all">Refund + Compensation + Legal Costs</option>
            </select>
          </div>

          <button 
            onClick={handleGenerate}
            disabled={status.loading}
            className="w-full py-4 bg-gray-900 hover:bg-gray-800 text-white font-bold text-lg rounded-xl shadow-lg transform transition-transform hover:scale-[1.01] flex items-center justify-center gap-2 focus:outline-none focus:ring-4 focus:ring-gray-300"
          >
            {status.loading ? <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" aria-hidden="true"></span> : "⚡ Generate Consumer Complaint — FREE"}
          </button>
        </div>
      </div>

      {/* Result Section */}
      {draft && (
        <div className="mt-8 bg-gray-50 border border-gray-200 rounded-2xl overflow-hidden animate-fade-in-up">
          <div className="bg-white px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <span className="font-bold text-gray-800">📄 Generated Complaint Draft</span>
            <button 
              onClick={() => navigator.clipboard.writeText(draft)}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-gray-300"
            >
              📋 Copy
            </button>
          </div>
          {/* React automatically escapes the content inside text nodes, preventing XSS here */}
          <div className="p-6 bg-white font-mono text-sm text-gray-800 whitespace-pre-wrap max-h-96 overflow-y-auto">
            {draft}
          </div>
          <div className="bg-orange-50 p-4 border-t border-orange-100 flex items-start gap-4">
            <div className="text-2xl" aria-hidden="true">⚠️</div>
            <div className="text-sm text-orange-800">
              <strong>Note:</strong> File at District Consumer Forum for claims up to ₹1 crore. 
              Claims ₹1Cr-₹10Cr → State Commission. Above ₹10Cr → National Commission. 
              No court fees for claims below ₹5 lakh.
              <a href="https://edaakhil.nic.in" target="_blank" rel="noopener noreferrer" className="block mt-2 font-bold text-orange-600 hover:underline">
                🌐 File on EDAAKHIL Portal →
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ConsumerCourt;
