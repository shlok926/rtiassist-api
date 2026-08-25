import React, { useState } from 'react';

const LabourComplaint = ({ setActiveTab }) => {
  const [formData, setFormData] = useState({
    employeeName: '',
    employerName: '',
    type: 'salary_unpaid',
    description: '',
    amount: '',
    state: ''
  });
  
  const [status, setStatus] = useState({ loading: false, error: null });
  const [draft, setDraft] = useState(null);

  const quickScenarios = [
    { label: '💸 Salary Not Paid', text: 'I worked as [Designation] for 6 months. Company fired me suddenly without notice and withheld my 2 months salary.' },
    { label: '📊 PF Not Deposited', text: 'PF is being deducted from my salary slips every month but the employer has not deposited it in my UAN account for 1 year.' },
    { label: '🚫 Wrongful Termination', text: 'Terminated without any valid reason and without the mandatory 30 days notice or pay in lieu of notice.' },
    { label: '🎁 Gratuity Denied', text: 'I worked continuously for 6 years and resigned. The company is refusing to pay my statutory gratuity amount.' }
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
    if (!formData.employeeName.trim()) return "Employee Name is required.";
    if (!formData.employerName.trim()) return "Employer Name is required.";
    if (!formData.description.trim()) return "Please describe the problem.";
    if (!formData.state) return "Please select the State.";
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
      setDraft(`BEFORE THE LABOUR COMMISSIONER / CONCILIATION OFFICER
Department of Labour, State of ${formData.state}

Subject: Complaint regarding ${formData.type.replace(/_/g, ' ')} against ${formData.employerName}

Respectfully Showeth:

1. COMPLAINANT DETAILS:
Name: ${formData.employeeName}

2. EMPLOYER / MANAGEMENT DETAILS:
Name: ${formData.employerName}

3. DETAILS OF DISPUTE / COMPLAINT:
${formData.description}
${formData.amount ? `Total amount due/claimed: ₹${formData.amount}` : ''}

4. GROUNDS OF COMPLAINT:
The aforementioned actions of the management are in clear violation of the Industrial Disputes Act, 1947 and the Payment of Wages Act, 1936. The management has adopted unfair labour practices causing severe financial hardship to the complainant.

5. PRAYER:
In view of the above, it is respectfully prayed that this Hon'ble Authority may be pleased to:
a) Intervene in the matter and summon the management for conciliation.
b) Direct the management to immediately release the dues / rectify the unlawful action.
c) Take strict penal action against the management for violating statutory labour laws.

Place: ${formData.state}
Date: ${new Date().toISOString().split('T')[0]}

Signature of Employee: _________________
Name: ${formData.employeeName}`);
      
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
      <div className="bg-gradient-to-r from-teal-800 to-teal-600 rounded-2xl p-6 md:p-10 mb-8 text-white shadow-xl flex flex-col md:flex-row items-center md:items-start gap-6">
        <div className="text-6xl" aria-hidden="true">💼</div>
        <div>
          <h2 className="text-2xl md:text-3xl font-black mb-3">Labour Complaint Generator</h2>
          <p className="text-teal-100 text-sm md:text-base mb-4 leading-relaxed">
            Boss ne salary nahi di? Bina notice ke nikaala? PF/ESI nahi kata? File formal complaint to Labour Commissioner / Industrial Tribunal — legally enforceable.
          </p>
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ Industrial Disputes Act 1947</span>
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ Payment of Wages Act</span>
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ Labour Commissioner Format</span>
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
              <label htmlFor="lc-name" className="block text-sm font-bold text-gray-700 mb-2">Employee Name *</label>
              <input 
                id="lc-name" type="text" name="employeeName" value={formData.employeeName} onChange={handleChange}
                placeholder="Your full name"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>
            <div>
              <label htmlFor="lc-employer" className="block text-sm font-bold text-gray-700 mb-2">Employer / Company Name *</label>
              <input 
                id="lc-employer" type="text" name="employerName" value={formData.employerName} onChange={handleChange}
                placeholder="Company/employer name"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="lc-type" className="block text-sm font-bold text-gray-700 mb-2">Type of Complaint *</label>
            <select 
              id="lc-type" name="type" value={formData.type} onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-teal-500 bg-white focus:outline-none"
            >
              <option value="salary_unpaid">Salary Not Paid / Withheld</option>
              <option value="wrongful_termination">Wrongful Termination (Without Notice)</option>
              <option value="pf_not_deposited">PF/EPF Not Deposited</option>
              <option value="esi_not_provided">ESI / Medical Benefits Not Given</option>
              <option value="overtime_unpaid">Overtime Not Paid</option>
              <option value="forced_resignation">Forced Resignation / Harassment</option>
              <option value="gratuity_denied">Gratuity Not Paid</option>
            </select>
          </div>

          {/* Scenarios */}
          <div>
            <span className="text-sm font-semibold text-gray-500 mb-2 block">💡 Common complaints — click to fill:</span>
            <div className="flex flex-wrap gap-2">
              {quickScenarios.map((sc, idx) => (
                <button 
                  key={idx} onClick={() => handleScenarioClick(sc.text)}
                  className="px-3 py-1.5 bg-teal-50 text-teal-700 text-sm font-medium rounded-full hover:bg-teal-100 transition-colors border border-teal-200 focus:outline-none focus:ring-2 focus:ring-teal-500"
                >
                  {sc.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="lc-desc" className="block text-sm font-bold text-gray-700 mb-2">Describe the Problem *</label>
            <textarea 
              id="lc-desc" name="description" value={formData.description} onChange={handleChange}
              rows="4" placeholder="Details: designation, joining date, amount owed, what happened..."
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-teal-500 resize-none focus:outline-none"
            ></textarea>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="lc-amount" className="block text-sm font-bold text-gray-700 mb-2">Amount Owed (₹) if applicable</label>
              <input 
                id="lc-amount" type="text" name="amount" value={formData.amount} onChange={handleChange}
                placeholder="e.g. 45000"
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-teal-500 focus:outline-none"
              />
            </div>
            <div>
              <label htmlFor="lc-state" className="block text-sm font-bold text-gray-700 mb-2">State *</label>
              <select 
                id="lc-state" name="state" value={formData.state} onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-teal-500 bg-white focus:outline-none"
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
            {status.loading ? <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full" aria-hidden="true"></span> : "⚡ Generate Labour Complaint — FREE"}
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
          <div className="p-6 bg-white font-mono text-sm text-gray-800 whitespace-pre-wrap max-h-96 overflow-y-auto">
            {draft}
          </div>
          <div className="bg-teal-50 p-4 border-t border-teal-200 flex items-start gap-4">
            <div className="text-2xl" aria-hidden="true">⚠️</div>
            <div className="text-sm text-teal-800">
              <strong>Note:</strong> Submit to the Labour Commissioner's office of your district. Bring original documents (offer letter, salary slips, bank statements). For PF issues, you can also directly complain on the <a href="https://epfindia.gov.in" target="_blank" rel="noopener noreferrer" className="font-bold underline">EPFO portal</a>.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default LabourComplaint;
