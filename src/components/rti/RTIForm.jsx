import React, { useState } from 'react';
import DraftResult from './DraftResult';
import LanguageModal from './LanguageModal';

const RTIForm = () => {
  const [description, setDescription] = useState('');
  const [state, setState] = useState('');
  const [category, setCategory] = useState('');
  const [isTipsOpen, setIsTipsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [resultData, setResultData] = useState(null);
  const [isLangModalOpen, setIsLangModalOpen] = useState(false);

  const quickExamples = [
    { label: '🍚 Ration Card', text: 'My ration card application was rejected 3 months ago and I want to know the exact reason, who rejected it, and see the complete file noting.' },
    { label: '📘 Passport', text: 'My passport application (File No: XX) is pending for 2 months. I want to know the current status, reasons for delay, and expected date of dispatch.' },
    { label: '👴 Pension', text: 'My father\'s pension has stopped coming since last 4 months. Please provide the reason, the officer responsible, and steps to resume it.' },
    { label: '🌾 Land Mutation', text: 'Applied for land mutation 6 months ago. What is the current status? Please provide copies of all internal file notings and reasons for delay.' },
    { label: '🎓 Scholarship', text: 'Applied for post-matric scholarship. Provide the status of my application, reasons if held up, and details of funds disbursed this year.' },
    { label: '💧 Water Supply', text: 'There is no water supply in my colony (Address) for the last 10 days. Provide copies of complaints received and action taken reports.' },
    { label: '🛣️ Road', text: 'Provide details of the contractor who built the road in (Area), total budget allocated, copy of the contract, and guarantee period.' },
    { label: '⚡ Electricity', text: 'Frequent power cuts in (Area). Provide log of power cuts in the last 30 days, reasons for outages, and maintenance schedule.' },
  ];

  const handleExampleClick = (text) => {
    setDescription(text);
  };

  const handleGenerateClick = () => {
    if (!description.trim()) {
      alert("Please describe what information you need.");
      return;
    }
    setIsLangModalOpen(true);
  };

  const executeGeneration = async (selectedLanguage) => {
    setIsLangModalOpen(false);
    setIsLoading(true);
    setError(null);
    setResultData(null);
    
    try {
      const response = await fetch('http://127.0.0.1:8000/rti/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          description: description,
          state: state || null,
          language: selectedLanguage,
          demo_mode: true // Force demo mode for instant responses
        }),
      });
      
      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate RTI application');
      }
      
      setResultData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setDescription('');
    setState('');
    setCategory('');
    setResultData(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className="bg-white p-6 md:p-8 rounded-2xl shadow-xl max-w-3xl w-full border border-gray-100 text-left relative overflow-hidden">
      {/* Header */}
      <div className="mb-6 border-b border-gray-100 pb-4">
        <div className="flex gap-2 mb-4">
          <div className="h-2 flex-1 bg-rti-blue rounded-full"></div>
          <div className="h-2 flex-1 bg-gray-100 rounded-full"></div>
          <div className="h-2 flex-1 bg-gray-100 rounded-full"></div>
        </div>
        <h2 className="text-2xl font-bold text-gray-800">Generate Your RTI Application</h2>
      </div>

      {/* Quick Examples */}
      <div className="mb-6">
        <span className="text-sm font-semibold text-gray-500 mb-2 block">💡 Quick examples — click to fill:</span>
        <div className="flex flex-wrap gap-2">
          {quickExamples.map((ex, idx) => (
            <button 
              key={idx}
              onClick={() => handleExampleClick(ex.text)}
              className="px-3 py-1.5 bg-blue-50 text-rti-blue text-sm rounded-full hover:bg-blue-100 transition-colors border border-blue-100"
            >
              {ex.label}
            </button>
          ))}
          <button className="px-3 py-1.5 text-gray-500 text-sm hover:text-gray-700 font-medium">
            📚 All Examples →
          </button>
        </div>
      </div>

      {/* Description Field */}
      <div className="mb-6">
        <label className="block text-sm font-bold text-gray-700 mb-2">
          Describe what information you need
        </label>
        <textarea 
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows="5"
          placeholder="Example: My ration card application was rejected 3 months ago in Maharashtra and I want to know the exact reason, who rejected it, and see the complete file noting..."
          className="w-full p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue focus:border-rti-blue transition-all resize-none text-gray-800"
        ></textarea>

        {/* Tips Box */}
        <div className="mt-3 bg-yellow-50 border border-yellow-200 rounded-xl overflow-hidden">
          <button 
            onClick={() => setIsTipsOpen(!isTipsOpen)}
            className="w-full px-4 py-3 flex items-center justify-between text-yellow-800 font-medium hover:bg-yellow-100 transition-colors"
          >
            <span className="text-sm">💡 Better description = stronger RTI — click for tips</span>
            <span className={`transform transition-transform ${isTipsOpen ? 'rotate-180' : ''}`}>▼</span>
          </button>
          
          <div className={`transition-all duration-300 ${isTipsOpen ? 'max-h-64 opacity-100' : 'max-h-0 opacity-0'} overflow-hidden`}>
            <ul className="p-4 pt-0 text-sm text-yellow-800 space-y-2">
              <li><span className="font-bold">📍 State name likho</span> — "Maharashtra mein", "Delhi ke"</li>
              <li><span className="font-bold">📅 Dates likho</span> — "3 months pehle", "January 2025 mein apply kiya"</li>
              <li><span className="font-bold">🔢 Numbers likho</span> — Application number, file number, case number</li>
              <li><span className="font-bold">👤 Officer name</span> — Kisi officer ne kuch bola ho toh unka naam mention karo</li>
              <li><span className="font-bold">❓ Specific poochho</span> — "Rejection ka reason", "kis officer ne reject kiya"</li>
              <li><span className="font-bold">📋 Problem clearly batao</span> — Jitna zyada context, utne specific questions AI banayega</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Selectors */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">State / Union Territory</label>
          <select 
            value={state}
            onChange={(e) => setState(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue bg-white text-gray-700"
          >
            <option value="">Central Government</option>
            <optgroup label="── States ──">
              <option>Andhra Pradesh</option><option>Maharashtra</option><option>Delhi</option>
              <option>Karnataka</option><option>Uttar Pradesh</option>
            </optgroup>
          </select>
        </div>
        <div>
          <label className="block text-sm font-bold text-gray-700 mb-2">Category (Optional)</label>
          <select 
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue bg-white text-gray-700"
          >
            <option value="">Auto-detect</option>
            <option>Food & Ration</option><option>Land & Revenue</option>
            <option>Passport & Visa</option><option>Pension & Social Security</option>
            <option>Education & Scholarship</option>
          </select>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl animate-fade-in">
          <strong>❌ Error:</strong> {error}
        </div>
      )}

      {/* Submit Button */}
      <button 
        onClick={handleGenerateClick}
        disabled={isLoading || resultData}
        className={`w-full py-4 px-6 font-bold text-lg rounded-xl shadow-lg transform transition-all flex items-center justify-center gap-2
          ${(isLoading || resultData) ? 'bg-gray-300 text-gray-500 cursor-not-allowed shadow-none' : 'bg-gradient-to-r from-rti-blue to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-blue-500/30 hover:scale-[1.02] active:scale-95'}
        `}
      >
        {isLoading ? (
          <>
            <span className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
            Generating...
          </>
        ) : resultData ? (
          "✅ Generated Successfully"
        ) : (
          "⚡ Generate RTI Application — Free"
        )}
      </button>

      {/* Result Section */}
      <DraftResult data={resultData} onReset={handleReset} />
      
      {/* Language Modal */}
      <LanguageModal 
        isOpen={isLangModalOpen} 
        onClose={() => setIsLangModalOpen(false)}
        onConfirm={executeGeneration}
      />
    </div>
  );
};

export default RTIForm;
