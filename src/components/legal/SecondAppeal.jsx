import React, { useState } from 'react';

const SecondAppeal = ({ setActiveTab }) => {
  const [formData, setFormData] = useState({
    name: '',
    rtiDate: '',
    appealDate: '',
    department: '',
    query: '',
    reason: 'no_response',
    details: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [draft, setDraft] = useState(null);

  const quickScenarios = [
    { label: '⏳ PIO No Reply', text: 'Filed RTI on time but PIO did not respond within the mandatory 30 days.' },
    { label: '🚫 FAA Also Ignored', text: 'First Appellate Authority (FAA) failed to pass an order within 30-45 days.' },
    { label: '❌ Wrong Exemption Cited', text: 'Information denied citing Section 8, but it does not apply to this public interest matter.' },
    { label: '🏛️ State Dept (SIC)', text: 'State government department. Information denied unlawfully.' },
    { label: '📁 Record Claimed Missing', text: 'PIO claimed the file is untraceable, which is unacceptable under the Act.' }
  ];

  const handleScenarioClick = (text) => {
    setFormData(prev => ({ ...prev, query: text }));
  };

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleGenerate = () => {
    if (!formData.name || !formData.rtiDate || !formData.department || !formData.query) {
      alert("Please fill all the required fields (*)");
      return;
    }

    setIsLoading(true);
    // Simulate API call for now
    setTimeout(() => {
      setDraft(`BEFORE THE CENTRAL INFORMATION COMMISSION
Second Appeal under Section 19(3) of the Right to Information Act, 2005

1. Name of the Appellant: ${formData.name}
2. Public Authority: ${formData.department}
3. Date of RTI Application: ${formData.rtiDate}
4. Date of First Appeal: ${formData.appealDate || 'N/A'}

Grounds for Second Appeal:
The appellant had sought information regarding: "${formData.query}".
However, the First Appeal was unsatisfactory because: ${formData.reason.replace(/_/g, ' ')}.
Additional Details: ${formData.details || 'None provided.'}

Prayer:
The appellant requests the Hon'ble Commission to direct the CPIO to provide the requested information free of cost under Section 7(6) and impose penalty under Section 20(1).

Signature:
Date: ${new Date().toISOString().split('T')[0]}`);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="w-full max-w-4xl mx-auto animate-fade-in text-left">
      <button 
        onClick={() => setActiveTab('legaltools')}
        className="mb-6 px-4 py-2 bg-white text-gray-600 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors font-medium text-sm"
      >
        ← Back to Legal Tools
      </button>

      {/* Hero */}
      <div className="bg-gradient-to-r from-blue-900 to-rti-blue rounded-2xl p-6 md:p-10 mb-8 text-white shadow-xl flex flex-col md:flex-row items-center md:items-start gap-6">
        <div className="text-6xl">📝</div>
        <div>
          <h2 className="text-2xl md:text-3xl font-black mb-3">Second Appeal — Central Information Commission</h2>
          <p className="text-blue-100 text-sm md:text-base mb-4 leading-relaxed">
            First Appeal rejected or ignored? File a Second Appeal to CIC under Section 19(3) of RTI Act 2005. 
            Lawyers charge ₹5000-15000 for this — we generate it FREE in 30 seconds.
          </p>
          <div className="flex flex-wrap gap-2">
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ Section 19(3) RTI Act 2005</span>
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ CIC Format</span>
            <span className="px-2 py-1 bg-white/20 rounded text-xs font-bold">✅ No Fee Required</span>
          </div>
        </div>
      </div>

      <div className="bg-white p-6 md:p-8 rounded-2xl shadow-xl border border-gray-100">
        <div className="space-y-6">
          
          <div className="form-group">
            <label className="block text-sm font-bold text-gray-700 mb-2">Your Full Name *</label>
            <input 
              type="text" name="name" value={formData.name} onChange={handleChange}
              placeholder="As per original RTI application"
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">Original RTI Application Date *</label>
              <input 
                type="date" name="rtiDate" value={formData.rtiDate} onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue text-gray-700"
              />
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-2">First Appeal Date *</label>
              <input 
                type="date" name="appealDate" value={formData.appealDate} onChange={handleChange}
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue text-gray-700"
              />
            </div>
          </div>

          <div className="form-group">
            <label className="block text-sm font-bold text-gray-700 mb-2">Public Authority / Department *</label>
            <input 
              type="text" name="department" value={formData.department} onChange={handleChange}
              placeholder="e.g. Ministry of Health, Food Dept Maharashtra"
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue"
            />
          </div>

          {/* Scenarios */}
          <div>
            <span className="text-sm font-semibold text-gray-500 mb-2 block">💡 Common scenarios — click to fill:</span>
            <div className="flex flex-wrap gap-2">
              {quickScenarios.map((sc, idx) => (
                <button 
                  key={idx} onClick={() => handleScenarioClick(sc.text)}
                  className="px-3 py-1.5 bg-blue-50 text-rti-blue text-sm rounded-full hover:bg-blue-100 transition-colors border border-blue-100"
                >
                  {sc.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label className="block text-sm font-bold text-gray-700 mb-2">Describe Your Original RTI Query *</label>
            <textarea 
              name="query" value={formData.query} onChange={handleChange}
              rows="3" placeholder="What information did you originally request? Be specific..."
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue resize-none"
            ></textarea>
          </div>

          <div className="form-group">
            <label className="block text-sm font-bold text-gray-700 mb-2">Why Was First Appeal Unsatisfactory?</label>
            <select 
              name="reason" value={formData.reason} onChange={handleChange}
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue bg-white text-gray-700"
            >
              <option value="no_response">First Appeal — No response received</option>
              <option value="incomplete">Information provided was incomplete</option>
              <option value="denied">Information denied without valid Section 8 reason</option>
              <option value="wrong_info">Wrong/incorrect information provided</option>
              <option value="partial">Only partial information given</option>
              <option value="delay">Responded after 30-day deadline</option>
            </select>
          </div>

          <div className="form-group">
            <label className="block text-sm font-bold text-gray-700 mb-2">Additional Details (optional)</label>
            <textarea 
              name="details" value={formData.details} onChange={handleChange}
              rows="2" placeholder="Any other relevant facts, evidence, or context..."
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue resize-none"
            ></textarea>
          </div>

          <button 
            onClick={handleGenerate}
            disabled={isLoading}
            className="w-full py-4 bg-gray-900 hover:bg-gray-800 text-white font-bold text-lg rounded-xl shadow-lg transform transition-transform hover:scale-[1.01] flex items-center justify-center gap-2"
          >
            {isLoading ? <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span> : "⚡ Generate Second Appeal — FREE"}
          </button>
        </div>
      </div>

      {/* Result Section */}
      {draft && (
        <div className="mt-8 bg-gray-50 border border-gray-200 rounded-2xl overflow-hidden animate-fade-in-up">
          <div className="bg-white px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <span className="font-bold text-gray-800">📄 Generated Appeal Draft</span>
            <div className="flex gap-2">
              <button 
                onClick={() => navigator.clipboard.writeText(draft)}
                className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-lg text-sm transition-colors"
              >
                📋 Copy
              </button>
            </div>
          </div>
          <div className="p-6 bg-white font-mono text-sm text-gray-800 whitespace-pre-wrap max-h-96 overflow-y-auto">
            {draft}
          </div>
          <div className="bg-orange-50 p-4 border-t border-orange-100 flex items-center gap-4">
            <div className="text-2xl">⚠️</div>
            <div className="text-sm text-orange-800">
              <strong>Note:</strong> You must attach copies of your original RTI, First Appeal, and any responses received. Sign the appeal and send it to CIC (New Delhi) or your State Information Commission.
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SecondAppeal;
