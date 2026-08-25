import React from 'react';

const LegalToolsHub = ({ setActiveTab }) => {
  return (
    <div className="w-full max-w-6xl mx-auto p-4 md:p-8 animate-fade-in">
      <div className="mb-8">
        <h2 className="text-3xl font-black text-gray-900 mb-2">⚖️ Legal Tools</h2>
        <p className="text-gray-600">Free AI-powered legal document generators — no lawyer needed</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        
        {/* Second Appeal */}
        <div 
          onClick={() => setActiveTab('second-appeal')}
          className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer relative overflow-hidden group"
        >
          <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform">📝</div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Second Appeal (CIC)</h3>
          <p className="text-gray-600 text-sm mb-6">First Appeal rejected? File a Second Appeal to Central Information Commission — free, auto-generated, legally correct.</p>
          <span className="inline-block px-3 py-1 bg-green-100 text-green-700 text-xs font-bold rounded-full">🏆 Highest Impact</span>
        </div>

        {/* Consumer Court */}
        <div 
          onClick={() => setActiveTab('consumer-court')}
          className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer relative overflow-hidden group"
        >
          <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform">🛒</div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Consumer Court Complaint</h3>
          <p className="text-gray-600 text-sm mb-6">Product defective, refund denied? File complaint to Consumer Forum via EDAAKHIL portal — AI generates perfect format.</p>
          <span className="inline-block px-3 py-1 bg-orange-100 text-orange-700 text-xs font-bold rounded-full">40L+ Pending Cases</span>
        </div>

        {/* Legal Notice */}
        <div 
          onClick={() => setActiveTab('legal-notice')}
          className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer relative overflow-hidden group"
        >
          <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform">📜</div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Legal Notice Generator</h3>
          <p className="text-gray-600 text-sm mb-6">Landlord not returning deposit? Builder delayed? Send a legal notice under specific IPC/CPC sections. Free.</p>
          <span className="inline-block px-3 py-1 bg-orange-100 text-orange-700 text-xs font-bold rounded-full">₹500Cr Market</span>
        </div>

        {/* Labour Complaint */}
        <div 
          onClick={() => setActiveTab('labour-complaint')}
          className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all cursor-pointer relative overflow-hidden group"
        >
          <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform">💼</div>
          <h3 className="text-xl font-bold text-gray-800 mb-2">Labour Complaint</h3>
          <p className="text-gray-600 text-sm mb-6">Salary not paid? Fired without notice? PF not deducted? File formal complaint to Labour Commissioner.</p>
          <span className="inline-block px-3 py-1 bg-gray-100 text-gray-700 text-xs font-bold rounded-full">10Cr+ Workers</span>
        </div>

        {/* Coming Soon */}
        <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200 opacity-60 cursor-not-allowed">
          <div className="text-4xl mb-4 grayscale">🏘️</div>
          <h3 className="text-xl font-bold text-gray-600 mb-2">Gram Panchayat Complaint</h3>
          <p className="text-gray-500 text-sm mb-6">MNREGA funds misused? Road/nali not built? File formal complaint to District Collector.</p>
          <span className="inline-block px-3 py-1 bg-gray-200 text-gray-600 text-xs font-bold rounded-full">Coming Soon</span>
        </div>

        {/* Coming Soon */}
        <div className="bg-gray-50 p-6 rounded-2xl border border-gray-200 opacity-60 cursor-not-allowed">
          <div className="text-4xl mb-4 grayscale">🔍</div>
          <h3 className="text-xl font-bold text-gray-600 mb-2">Tender Objection (CVC)</h3>
          <p className="text-gray-500 text-sm mb-6">Government tender irregularity? File CVC complaint + RTI for tender documents combo.</p>
          <span className="inline-block px-3 py-1 bg-gray-200 text-gray-600 text-xs font-bold rounded-full">Coming Soon</span>
        </div>

      </div>

      <div className="bg-green-50/50 border border-green-100 rounded-2xl p-6 text-center">
        <p className="text-gray-600">
          All tools are <strong className="text-rti-green font-bold">100% FREE</strong>. No signup. No hidden charges. 
          Lawyers charge ₹2000-15000 for these documents — we generate them in 30 seconds.
        </p>
      </div>
    </div>
  );
};

export default LegalToolsHub;
