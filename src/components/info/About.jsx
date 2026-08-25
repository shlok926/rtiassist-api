import React from 'react';

const About = () => {
  return (
    <div className="w-full max-w-5xl mx-auto p-4 md:p-8 animate-fade-in text-left">
      
      {/* Hero */}
      <div className="text-center mb-16">
        <h2 className="text-4xl md:text-5xl font-black text-gray-900 mb-4">
          🏛️ About <span className="text-transparent bg-clip-text bg-gradient-to-r from-orange-500 to-orange-600">RTIAssist</span>
        </h2>
        <p className="text-gray-600 text-lg md:text-xl max-w-3xl mx-auto leading-relaxed">
          India's most powerful free AI-powered tool to help citizens exercise their fundamental Right to Information under the RTI Act, 2005.
        </p>
      </div>

      {/* Mission Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
        <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:-translate-y-1 transition-transform">
          <div className="text-4xl mb-4">🎯</div>
          <h4 className="text-xl font-bold text-gray-900 mb-3">Our Mission</h4>
          <p className="text-gray-600 leading-relaxed">
            Empower every Indian citizen to hold the government accountable by making RTI filing simple, fast, and free — in any Indian language.
          </p>
        </div>
        <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:-translate-y-1 transition-transform">
          <div className="text-4xl mb-4">💡</div>
          <h4 className="text-xl font-bold text-gray-900 mb-3">Why RTIAssist?</h4>
          <p className="text-gray-600 leading-relaxed">
            Filing RTI shouldn't require legal expertise. Our AI understands your complaint in plain language and generates a legally-correct application in 30 seconds.
          </p>
        </div>
        <div className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:-translate-y-1 transition-transform">
          <div className="text-4xl mb-4">🌍</div>
          <h4 className="text-xl font-bold text-gray-900 mb-3">Open Source</h4>
          <p className="text-gray-600 leading-relaxed">
            RTIAssist is 100% free and open source under MIT License. Anyone can contribute, audit, or deploy their own instance.
          </p>
        </div>
      </div>

      {/* Features Overview */}
      <div className="mb-16">
        <h3 className="text-3xl font-black text-gray-900 mb-8 text-center">⚡ What RTIAssist Does</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200">
            <div className="text-3xl mb-3">📝</div>
            <h4 className="text-lg font-bold text-gray-900 mb-2">AI Draft Generator</h4>
            <p className="text-gray-600 text-sm">Describe your problem in plain words. AI identifies the right department, PIO, and generates a legally-correct RTI application.</p>
          </div>
          <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200">
            <div className="text-3xl mb-3">🌐</div>
            <h4 className="text-lg font-bold text-gray-900 mb-2">11 Indian Languages</h4>
            <p className="text-gray-600 text-sm">Generate RTI in Hindi, English, Marathi, Tamil, Telugu, Kannada, Bengali, Gujarati, Punjabi, Malayalam, or Odia.</p>
          </div>
          <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200">
            <div className="text-3xl mb-3">📊</div>
            <h4 className="text-lg font-bold text-gray-900 mb-2">Quality Scoring</h4>
            <p className="text-gray-600 text-sm">Every draft gets a quality score with suggestions to improve. Aim for 70+ for best results.</p>
          </div>
          <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200">
            <div className="text-3xl mb-3">⚖️</div>
            <h4 className="text-lg font-bold text-gray-900 mb-2">Exemption Check</h4>
            <p className="text-gray-600 text-sm">Automatically checks Section 8 exemptions so your RTI isn't rejected. Get warnings before filing.</p>
          </div>
          <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200">
            <div className="text-3xl mb-3">📋</div>
            <h4 className="text-lg font-bold text-gray-900 mb-2">RTI Tracker</h4>
            <p className="text-gray-600 text-sm">Save, track, and manage all your RTIs in one place. Monitor 30-day deadlines and response status locally.</p>
          </div>
          <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200">
            <div className="text-3xl mb-3">📝</div>
            <h4 className="text-lg font-bold text-gray-900 mb-2">Appeal Generator</h4>
            <p className="text-gray-600 text-sm">If PIO doesn't respond in 30 days, generate a First Appeal or Second Appeal letter with one click.</p>
          </div>
        </div>
      </div>

      {/* Tech Stack */}
      <div className="mb-16 bg-gray-900 rounded-3xl p-8 md:p-12 text-white text-center shadow-2xl relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-rti-blue rounded-full filter blur-[100px] opacity-20 -translate-y-1/2 translate-x-1/2"></div>
        <div className="absolute bottom-0 left-0 w-64 h-64 bg-rti-green rounded-full filter blur-[100px] opacity-20 translate-y-1/2 -translate-x-1/2"></div>
        
        <h3 className="text-3xl font-black mb-10 relative z-10">🔧 Technology Stack</h3>
        <div className="flex flex-wrap justify-center gap-6 relative z-10">
          <div className="bg-white/10 backdrop-blur border border-white/20 p-6 rounded-2xl w-40 hover:bg-white/20 transition-colors">
            <div className="text-4xl mb-3">⚛️</div>
            <div className="font-bold">React</div>
            <div className="text-xs text-gray-300 mt-1">Frontend</div>
          </div>
          <div className="bg-white/10 backdrop-blur border border-white/20 p-6 rounded-2xl w-40 hover:bg-white/20 transition-colors">
            <div className="text-4xl mb-3">🌊</div>
            <div className="font-bold">Tailwind</div>
            <div className="text-xs text-gray-300 mt-1">Styling</div>
          </div>
          <div className="bg-white/10 backdrop-blur border border-white/20 p-6 rounded-2xl w-40 hover:bg-white/20 transition-colors">
            <div className="text-4xl mb-3">🐍</div>
            <div className="font-bold">FastAPI</div>
            <div className="text-xs text-gray-300 mt-1">Python Backend</div>
          </div>
          <div className="bg-white/10 backdrop-blur border border-white/20 p-6 rounded-2xl w-40 hover:bg-white/20 transition-colors">
            <div className="text-4xl mb-3">🤖</div>
            <div className="font-bold">AI Engine</div>
            <div className="text-xs text-gray-300 mt-1">Reasoning Pipeline</div>
          </div>
        </div>
      </div>

      {/* Privacy Commitment */}
      <div className="mb-16 bg-green-50 border border-green-200 rounded-3xl p-8 md:p-12 shadow-sm">
        <div className="flex items-center gap-4 mb-6">
          <div className="text-4xl">🔒</div>
          <h3 className="text-2xl font-black text-green-900">Privacy Commitment</h3>
        </div>
        <ul className="space-y-4 text-green-800">
          <li className="flex items-start gap-3"><span className="text-green-600 font-bold">✓</span> No personal data is stored on our servers</li>
          <li className="flex items-start gap-3"><span className="text-green-600 font-bold">✓</span> All user settings and tracker data are saved locally in your browser</li>
          <li className="flex items-start gap-3"><span className="text-green-600 font-bold">✓</span> RTI drafts are generated on-the-fly and not logged</li>
          <li className="flex items-start gap-3"><span className="text-green-600 font-bold">✓</span> No tracking, no analytics, no cookies</li>
          <li className="flex items-start gap-3"><span className="text-green-600 font-bold">✓</span> Open source — audit the code yourself on GitHub</li>
          <li className="flex items-start gap-3"><span className="text-green-600 font-bold">✓</span> No signup or login required</li>
        </ul>
      </div>

      {/* Contact & Support */}
      <div className="mb-16">
        <h3 className="text-3xl font-black text-gray-900 mb-8 text-center">📞 Contact & Support</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <a href="mailto:support@rtiassist.in" className="flex flex-col items-center p-6 bg-white rounded-2xl shadow border border-gray-100 hover:shadow-md transition-shadow group">
            <div className="text-3xl mb-3 group-hover:scale-110 transition-transform">📧</div>
            <div className="font-bold text-gray-900">Email</div>
            <div className="text-sm text-gray-500">support@rtiassist.in</div>
          </a>
          <a href="https://github.com/shlok926/RTIASSIST-API" target="_blank" rel="noopener noreferrer" className="flex flex-col items-center p-6 bg-white rounded-2xl shadow border border-gray-100 hover:shadow-md transition-shadow group">
            <div className="text-3xl mb-3 group-hover:scale-110 transition-transform">💻</div>
            <div className="font-bold text-gray-900">GitHub</div>
            <div className="text-sm text-gray-500">View Source Code</div>
          </a>
          <a href="https://github.com/shlok926/RTIASSIST-API/discussions" target="_blank" rel="noopener noreferrer" className="flex flex-col items-center p-6 bg-white rounded-2xl shadow border border-gray-100 hover:shadow-md transition-shadow group">
            <div className="text-3xl mb-3 group-hover:scale-110 transition-transform">💬</div>
            <div className="font-bold text-gray-900">Community</div>
            <div className="text-sm text-gray-500">Discussions</div>
          </a>
          <a href="https://github.com/shlok926/RTIASSIST-API/issues" target="_blank" rel="noopener noreferrer" className="flex flex-col items-center p-6 bg-white rounded-2xl shadow border border-gray-100 hover:shadow-md transition-shadow group">
            <div className="text-3xl mb-3 group-hover:scale-110 transition-transform">🐛</div>
            <div className="font-bold text-gray-900">Report Bug</div>
            <div className="text-sm text-gray-500">Issues</div>
          </a>
        </div>
      </div>

      {/* Legal Disclaimer */}
      <div className="bg-orange-50 border border-orange-200 rounded-2xl p-6 md:p-8 text-center text-orange-900">
        <h4 className="font-bold text-lg mb-2">⚠️ Legal Disclaimer</h4>
        <p className="text-sm leading-relaxed max-w-4xl mx-auto">
          RTIAssist is a free tool that helps generate RTI applications. It is <strong>not legal advice</strong>. 
          The generated drafts should be reviewed before submission. We are not affiliated with any government body. 
          The Right to Information Act, 2005 is a law enacted by the Parliament of India, and RTIAssist simply helps citizens exercise this right more effectively.
        </p>
      </div>

    </div>
  );
};

export default About;
