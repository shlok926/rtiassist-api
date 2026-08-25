import React, { useState } from 'react';

const ExamplesLibrary = ({ setActiveTab }) => {
  const [activeSubTab, setActiveSubTab] = useState('rti');
  const [filter, setFilter] = useState('all');

  const rtiExamples = [
    { cat: 'Food', title: 'Ration Card Not Issued', text: 'I applied for a new ration card 3 months ago. I want to know the exact reason why it is delayed and who is the officer responsible.' },
    { cat: 'Land', title: 'Property Mutation Status', text: 'Application for property mutation is pending. I need certified copies of file notings regarding my application.' },
    { cat: 'Travel', title: 'Passport Police Verification', text: 'My passport police verification is pending for 45 days. I need to know the current status and daily progress made.' },
    { cat: 'Education', title: 'Scholarship Not Disbursed', text: 'My post-matric scholarship was approved but not credited. I need the disbursement status and delay reasons.' },
    { cat: 'Pension', title: 'Widow Pension Stopped', text: 'My widow pension has been stopped without any notice for the last 6 months. I need the order copy.' },
    { cat: 'Municipal', title: 'Road Repair Work Details', text: 'I need details of funds allocated and spent on repairing the main road in my ward over the last 1 year.' },
    { cat: 'Police', title: 'FIR Copy Not Provided', text: 'I filed a complaint last week but was not given an FIR copy. I want the status of my complaint and action taken.' },
  ];

  const legalExamples = [
    { cat: 'consumer', title: 'E-commerce Refund', text: 'Ordered product online but received empty box. Company refusing refund despite multiple complaints.' },
    { cat: 'legal_notice', title: 'Security Deposit', text: 'I vacated the flat after giving 1 month notice. Landlord is not returning my security deposit of ₹50,000.' },
    { cat: 'labour', title: 'Salary Not Paid', text: 'Company fired me suddenly without notice and withheld my 2 months salary.' },
    { cat: 'second_appeal', title: 'PIO No Reply', text: 'Filed RTI on time but PIO did not respond within the mandatory 30 days.' }
  ];

  const handleUseExample = (text, type) => {
    // In a real implementation, this would pass the text to the respective form state.
    // For now, we'll route to the right page. The user can copy the text or we can use Context.
    alert(`Copied to clipboard!\n\n"${text}"\n\nRouting to the ${type} form...`);
    navigator.clipboard.writeText(text);
    setActiveTab(type === 'rti' ? 'home' : type);
  };

  const currentRTI = filter === 'all' ? rtiExamples : rtiExamples.filter(e => e.cat === filter);
  const currentLegal = filter === 'all' ? legalExamples : legalExamples.filter(e => e.cat === filter);

  return (
    <div className="w-full max-w-6xl mx-auto p-4 md:p-8 animate-fade-in text-left">
      {/* Hero */}
      <div className="text-center mb-12">
        <div className="text-5xl mb-4">💡</div>
        <h2 className="text-3xl md:text-4xl font-black text-gray-900 mb-4">Examples Library</h2>
        <p className="text-gray-600 text-lg max-w-2xl mx-auto">
          Click "Use This" on any example to copy the text and jump to the generator. Based on real Indian scenarios.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex justify-center gap-4 mb-8">
        <button 
          onClick={() => { setActiveSubTab('rti'); setFilter('all'); }}
          className={`px-6 py-2 font-bold rounded-full transition-colors ${activeSubTab === 'rti' ? 'bg-rti-blue text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
        >
          RTI Examples
        </button>
        <button 
          onClick={() => { setActiveSubTab('legal'); setFilter('all'); }}
          className={`px-6 py-2 font-bold rounded-full transition-colors ${activeSubTab === 'legal' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
        >
          Legal Tools Examples
        </button>
      </div>

      {activeSubTab === 'rti' && (
        <>
          <div className="flex flex-wrap justify-center gap-2 mb-8">
            {['all', 'Food', 'Land', 'Travel', 'Education', 'Pension', 'Municipal', 'Police'].map(c => (
              <button 
                key={c} onClick={() => setFilter(c)}
                className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${filter === c ? 'bg-blue-100 text-blue-800 border border-blue-200' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'}`}
              >
                {c === 'all' ? 'All' : c}
              </button>
            ))}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {currentRTI.map((ex, idx) => (
              <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow flex flex-col">
                <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded w-fit mb-3">{ex.cat}</span>
                <h3 className="font-bold text-gray-900 mb-2">{ex.title}</h3>
                <p className="text-gray-600 text-sm italic mb-6 flex-grow">"{ex.text}"</p>
                <button 
                  onClick={() => handleUseExample(ex.text, 'home')}
                  className="w-full py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 font-bold rounded-lg text-sm transition-colors"
                >
                  Use This →
                </button>
              </div>
            ))}
          </div>
        </>
      )}

      {activeSubTab === 'legal' && (
        <>
          <div className="flex flex-wrap justify-center gap-2 mb-8">
            {['all', 'consumer', 'legal_notice', 'labour', 'second_appeal'].map(c => (
              <button 
                key={c} onClick={() => setFilter(c)}
                className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-colors capitalize ${filter === c ? 'bg-gray-800 text-white border border-gray-800' : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'}`}
              >
                {c.replace('_', ' ')}
              </button>
            ))}
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {currentLegal.map((ex, idx) => (
              <div key={idx} className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow flex flex-col">
                <span className="text-xs font-bold text-gray-600 bg-gray-100 px-2 py-1 rounded w-fit mb-3 capitalize">{ex.cat.replace('_', ' ')}</span>
                <h3 className="font-bold text-gray-900 mb-2">{ex.title}</h3>
                <p className="text-gray-600 text-sm italic mb-6 flex-grow">"{ex.text}"</p>
                <button 
                  onClick={() => handleUseExample(ex.text, ex.cat === 'consumer' ? 'consumer-court' : ex.cat === 'legal_notice' ? 'legal-notice' : ex.cat === 'labour' ? 'labour-complaint' : 'second-appeal')}
                  className="w-full py-2 bg-gray-900 hover:bg-gray-800 text-white font-bold rounded-lg text-sm transition-colors"
                >
                  Use This →
                </button>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default ExamplesLibrary;
