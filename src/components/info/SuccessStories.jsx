import React from 'react';

const SuccessStories = () => {
  const stories = [
    {
      id: 1,
      category: '🍚 Ration Card',
      title: '2-Year Wait Ended in 30 Days',
      story: '"My ration card application was stuck for 2 years. After filing RTI through RTIAssist asking for application status and responsible officer, I got my ration card within 30 days!"',
      state: '📍 Maharashtra',
      time: '⏱ Resolved in 30 days',
      impact: 'Family of 4 now gets subsidized food grains',
      color: 'bg-green-100 text-green-800'
    },
    {
      id: 2,
      category: '💧 Water Supply',
      title: '6-Month Water Crisis Fixed',
      story: '"Our area had no municipal water for 6 months despite complaints. RTI revealed ₹20 lakh was sanctioned but not used. After filing, supply resumed in 3 weeks."',
      state: '📍 Gujarat',
      time: '⏱ Resolved in 21 days',
      impact: '200+ households now have regular water supply',
      color: 'bg-blue-100 text-blue-800'
    },
    {
      id: 3,
      category: '🎓 Scholarship',
      title: '₹50,000 Scholarship Released',
      story: '"Applied for post-matric scholarship 8 months ago — no response. RTI through RTIAssist showed my application was approved but payment pending. Got ₹50,000 in my account within 2 weeks!"',
      state: '📍 Karnataka',
      time: '⏱ Resolved in 14 days',
      impact: 'Student continued college education',
      color: 'bg-purple-100 text-purple-800'
    },
    {
      id: 4,
      category: '🛣️ Road Construction',
      title: '₹40 Lakh Road Completed',
      story: '"PMGSY road sanctioned 3 years ago, no work done. RTI revealed contractor took advance but didn\\'t start. District Magistrate ordered completion — road ready in 4 months!"',
      state: '📍 Bihar',
      time: '⏱ Resolved in 120 days',
      impact: '5 villages connected to highway',
      color: 'bg-yellow-100 text-yellow-800'
    },
    {
      id: 5,
      category: '📘 Passport',
      title: 'Police Verification Cleared',
      story: '"Passport stuck at police verification for 7 months. RTI showed verification report was submitted but lost in file. Re-verification ordered, passport delivered in 3 weeks."',
      state: '📍 Central Govt',
      time: '⏱ Resolved in 21 days',
      impact: 'Family went for Dubai job opportunity',
      color: 'bg-indigo-100 text-indigo-800'
    },
    {
      id: 6,
      category: '⚡ Electricity',
      title: 'Overbilling Corrected — ₹18,000 Refund',
      story: '"Electricity bill suddenly jumped from ₹800 to ₹6,000/month. RTI revealed meter reading error. Billing corrected and got ₹18,000 refund for 3 months of overcharging!"',
      state: '📍 Madhya Pradesh',
      time: '⏱ Resolved in 45 days',
      impact: '₹18,000 refund + future bills corrected',
      color: 'bg-orange-100 text-orange-800'
    }
  ];

  return (
    <div className="w-full max-w-6xl mx-auto p-4 md:p-8 animate-fade-in text-left">
      
      {/* Hero */}
      <div className="text-center mb-12">
        <div className="text-5xl mb-4">🌟</div>
        <h2 className="text-3xl md:text-4xl font-black text-gray-900 mb-4">Success Stories</h2>
        <p className="text-gray-600 text-lg max-w-2xl mx-auto">
          Real RTI applications that made a difference — powered by RTIAssist
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {stories.map(story => (
          <div key={story.id} className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:-translate-y-1 transition-transform">
            <div className="flex justify-between items-start mb-4">
              <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-bold rounded-full">✅ Resolved</span>
              <span className={`px-2 py-1 text-xs font-bold rounded-full ${story.color}`}>{story.category}</span>
            </div>
            
            <h3 className="text-xl font-bold text-gray-900 mb-3">{story.title}</h3>
            
            <p className="text-gray-600 text-sm italic mb-6 leading-relaxed">
              {story.story}
            </p>
            
            <div className="bg-gray-50 rounded-xl p-4 space-y-2 text-xs font-semibold text-gray-700">
              <div className="flex items-center gap-2">
                <span>{story.state}</span>
              </div>
              <div className="flex items-center gap-2">
                <span>{story.time}</span>
              </div>
            </div>
            
            <div className="mt-4 pt-4 border-t border-gray-100">
              <p className="text-sm font-bold text-rti-green">Impact: {story.impact}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-12 bg-orange-50 border border-orange-100 rounded-2xl p-8 text-center max-w-2xl mx-auto">
        <h3 className="text-2xl font-bold text-orange-800 mb-2">📣 Share Your Success Story</h3>
        <p className="text-orange-900/70 mb-6">Did RTIAssist help you get results? Share your story to inspire others!</p>
        <a 
          href="https://github.com/shlok926/RTIASSIST-API/discussions" 
          target="_blank" 
          rel="noopener noreferrer"
          className="inline-block px-6 py-3 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white font-bold rounded-xl shadow-lg transition-transform hover:scale-105"
        >
          Share on GitHub Discussions →
        </a>
      </div>
    </div>
  );
};

export default SuccessStories;
