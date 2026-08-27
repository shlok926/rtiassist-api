import React, { useState, useEffect } from 'react';

const Settings = () => {
  const [profile, setProfile] = useState({
    name: '', phone: '', email: '', address: '', city: '', pincode: '', state: ''
  });
  const [feedback, setFeedback] = useState({ rating: 0, comment: '', email: '' });
  const [showFeedbackSuccess, setShowFeedbackSuccess] = useState(false);
  const [openFaq, setOpenFaq] = useState(null);

    const handleClear = () => {
    if (window.confirm('Are you sure you want to clear your local session?')) {
      localStorage.removeItem('token');
      window.location.reload();
    }
  };

  const handleFeedbackSubmit = () => {
    if (feedback.rating === 0) {
      alert('Please select a star rating first.');
      return;
    }
    // Simulate submission
    setTimeout(() => {
      setShowFeedbackSuccess(true);
      setFeedback({ rating: 0, comment: '', email: '' });
      setTimeout(() => setShowFeedbackSuccess(false), 5000);
    }, 1000);
  };

  const faqs = [
    { q: "How do I file my RTI after generating the draft?", a: "Online: Go to rtionline.gov.in, register, paste your draft, pay ₹10 online.\n\nBy Post: Print the draft, attach ₹10 Indian Postal Order (IPO), send by Speed Post to the PIO mentioned in filing instructions." },
    { q: "Is RTIAssist really free?", a: "Yes — 100% free, forever. RTIAssist is open-source. No subscription, no hidden charges. The only cost is ₹10 RTI filing fee paid directly to the government." },
    { q: "Is my data safe?", a: "Yes. Your personal details are saved only in your browser's localStorage — never uploaded to any server. Only your problem description is sent to the AI to generate the draft, via encrypted API calls." },
    { q: "What if the PIO doesn't respond in 30 days?", a: "File a First Appeal under Section 19(1) of RTI Act 2005. Use the \"Generate First Appeal Letter\" button from your Tracker. If First Appeal also fails, file a Second Appeal to CIC/SIC using the Legal Tools section." }
  ];

  return (
    <div className="w-full max-w-5xl mx-auto p-4 md:p-8 animate-fade-in text-left">
      <div className="mb-10">
        <h2 className="text-3xl font-black text-gray-900 mb-2">⚙️ Settings & Profile</h2>
        <p className="text-gray-600">Save your details to auto-fill RTI applications. All data is stored locally in your browser.</p>
      </div>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 md:p-8 mb-8">
        <div className="mt-8 p-4 bg-red-50 border border-red-100 rounded-xl flex items-center justify-between">
          <div className="text-sm text-red-800">
            <strong>Danger Zone:</strong> Clear local authentication session.
          </div>
          <button onClick={handleClear} className="px-4 py-2 bg-white text-red-600 border border-red-200 font-bold rounded-lg hover:bg-red-50 transition-colors">
            🗑️ Logout
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Notifications & Feedback */}
        <div className="space-y-8">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">🔔 Notifications</h3>
            <div className="p-4 bg-blue-50 border border-blue-100 rounded-xl flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <div className="font-bold text-blue-900">Telegram Reminders</div>
                <div className="text-sm text-blue-700">Bot sends you a message 7 days and 1 day before your RTI deadline.</div>
              </div>
              <a href="https://t.me/RTIAssistBot" target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-blue-600 text-white font-bold rounded-lg hover:bg-blue-700 transition-colors whitespace-nowrap">
                Open Bot →
              </a>
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">⭐ Feedback</h3>
            <div className="mb-4">
              <div className="text-sm text-gray-500 mb-2">Overall Rating:</div>
              <div className="flex gap-2">
                {[1,2,3,4,5].map(star => (
                  <button 
                    key={star} 
                    onClick={() => setFeedback(prev => ({ ...prev, rating: star }))}
                    className={`text-2xl transition-transform hover:scale-110 ${feedback.rating >= star ? 'grayscale-0' : 'grayscale opacity-30'}`}
                  >
                    ⭐
                  </button>
                ))}
              </div>
            </div>
            <textarea 
              value={feedback.comment} onChange={e => setFeedback(prev => ({ ...prev, comment: e.target.value }))}
              placeholder="What did you like? What can be improved?" 
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue mb-4 resize-none" rows="3"
            ></textarea>
            <input 
              type="email" value={feedback.email} onChange={e => setFeedback(prev => ({ ...prev, email: e.target.value }))}
              placeholder="Your email (optional)" 
              className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-rti-blue mb-4"
            />
            <button onClick={handleFeedbackSubmit} className="w-full py-3 bg-gray-900 text-white font-bold rounded-xl hover:bg-gray-800 transition-colors">
              📤 Submit Feedback
            </button>
            {showFeedbackSuccess && (
              <div className="mt-4 p-3 bg-green-50 text-green-700 text-sm font-medium rounded-lg text-center animate-fade-in">
                🙏 Thank you! Your feedback has been received.
              </div>
            )}
          </div>
        </div>

        {/* FAQs */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
          <h3 className="text-xl font-bold text-gray-900 mb-6">❓ Help & Support</h3>
          <div className="space-y-4">
            {faqs.map((faq, i) => (
              <div key={i} className="border border-gray-200 rounded-xl overflow-hidden">
                <button 
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  className="w-full p-4 text-left font-bold text-gray-800 bg-gray-50 hover:bg-gray-100 flex justify-between items-center transition-colors"
                >
                  {faq.q}
                  <span className={`transform transition-transform ${openFaq === i ? 'rotate-180' : ''}`}>▼</span>
                </button>
                {openFaq === i && (
                  <div className="p-4 text-gray-600 text-sm bg-white whitespace-pre-wrap border-t border-gray-100">
                    {faq.a}
                  </div>
                )}
              </div>
            ))}
          </div>
          
          <div className="mt-8 flex flex-wrap gap-3">
            <a href="https://github.com/shlok926/rtiassist-api/issues" target="_blank" rel="noopener noreferrer" className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-bold transition-colors">
              🐛 Report Bug
            </a>
            <a href="mailto:support@rtiassist.in" className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-bold transition-colors">
              📧 Contact Support
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
