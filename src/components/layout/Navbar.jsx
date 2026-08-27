import React, { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

const Navbar = ({ activeTab, setActiveTab, onOpenAuth }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isLegalMenuOpen, setIsLegalMenuOpen] = useState(false);
  const [isBellOpen, setIsBellOpen] = useState(false);
  const { user, logout } = useAuth();

  const showPage = (page) => {
    setActiveTab(page);
    setIsMobileMenuOpen(false);
  };
  const toggleUILanguage = () => console.log('Toggle language');

  return (
    <nav className="flex items-center justify-between px-6 py-4 bg-white/95 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50 shadow-sm transition-all duration-300">
      {/* Logo */}
      <div 
        className="flex items-center gap-2 cursor-pointer transition-transform hover:scale-105"
        onClick={() => showPage('home')}
      >
        <div className="flex items-center justify-center w-10 h-10 bg-rti-blue text-white rounded-xl shadow-md text-xl">
          🏛
        </div>
        <div className="font-serif font-black text-2xl tracking-tight text-gray-900">
          RTI<span className="text-rti-green">Assist</span>
        </div>
      </div>

      {/* Hamburger */}
      <button 
        className="md:hidden text-2xl p-2 rounded-lg hover:bg-gray-100 transition-colors"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        ☰
      </button>

      {/* Nav Links */}
      <div className={`
        absolute md:static top-full left-0 w-full md:w-auto bg-white md:bg-transparent
        flex flex-col md:flex-row items-stretch md:items-center gap-2 md:gap-4 p-4 md:p-0
        shadow-lg md:shadow-none border-b md:border-none border-gray-100
        transition-all duration-300 ease-in-out
        ${isMobileMenuOpen ? 'opacity-100 visible' : 'opacity-0 invisible md:opacity-100 md:visible'}
      `}>
        <button 
          onClick={() => showPage('home')} 
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${activeTab === 'home' ? 'text-rti-blue bg-blue-50' : 'text-gray-600 hover:bg-gray-50'}`}
        >
          🏠 RTI
        </button>
        <button 
          onClick={() => showPage('tracker')} 
          className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${activeTab === 'tracker' ? 'text-rti-blue bg-blue-50' : 'text-gray-600 hover:bg-gray-50'}`}
        >
          📋 My RTIs
        </button>
        
        {/* Dropdown */}
        <div className="relative group">
          <button 
            className="w-full md:w-auto px-4 py-2 text-sm font-medium rounded-lg text-gray-600 hover:bg-gray-50 transition-colors flex items-center justify-between gap-1"
            onClick={() => setIsLegalMenuOpen(!isLegalMenuOpen)}
            onMouseEnter={() => setIsLegalMenuOpen(true)}
            onMouseLeave={() => setIsLegalMenuOpen(false)}
          >
            ⚖️ Legal Tools <span className="text-xs text-gray-400">▼</span>
          </button>
          
          <div 
            className={`
              md:absolute left-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-50
              transition-all duration-200 transform origin-top
              ${isLegalMenuOpen ? 'scale-100 opacity-100 visible' : 'scale-95 opacity-0 invisible'}
            `}
            onMouseEnter={() => setIsLegalMenuOpen(true)}
            onMouseLeave={() => setIsLegalMenuOpen(false)}
          >
            <div className="py-2">
              <button onClick={() => showPage('legaltools')} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-3">
                <span className="text-lg">🧰</span> All Legal Tools
              </button>
              <div className="h-px bg-gray-100 my-1"></div>
              <button onClick={() => showPage('second-appeal')} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between">
                <div className="flex items-center gap-3"><span className="text-lg">📝</span> Second Appeal</div>
                <span className="text-[10px] font-bold px-2 py-0.5 bg-green-100 text-green-700 rounded-full">FREE</span>
              </button>
              <button onClick={() => showPage('consumer-court')} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between">
                <div className="flex items-center gap-3"><span className="text-lg">🛒</span> Consumer Court</div>
                <span className="text-[10px] font-bold px-2 py-0.5 bg-green-100 text-green-700 rounded-full">FREE</span>
              </button>
              <button onClick={() => showPage('legal-notice')} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between">
                <div className="flex items-center gap-3"><span className="text-lg">📜</span> Legal Notice</div>
                <span className="text-[10px] font-bold px-2 py-0.5 bg-green-100 text-green-700 rounded-full">FREE</span>
              </button>
              <button onClick={() => showPage('labour-complaint')} className="w-full text-left px-4 py-2.5 text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between">
                <div className="flex items-center gap-3"><span className="text-lg">💼</span> Labour Complaint</div>
                <span className="text-[10px] font-bold px-2 py-0.5 bg-green-100 text-green-700 rounded-full">FREE</span>
              </button>
            </div>
          </div>
        </div>

        <button onClick={() => showPage('fees')} className="px-4 py-2 text-sm font-medium rounded-lg text-gray-600 hover:bg-gray-50 transition-colors">💰 Fees</button>
        <button onClick={() => showPage('examples')} className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${activeTab === 'examples' ? 'text-rti-blue bg-blue-50' : 'text-gray-600 hover:bg-gray-50'}`}>💡 Examples</button>
        <button onClick={() => showPage('settings')} className={`px-4 py-2 text-sm font-medium rounded-lg transition-colors ${activeTab === 'settings' ? 'text-rti-blue bg-blue-50' : 'text-gray-600 hover:bg-gray-50'}`}>⚙️ Settings</button>
        
        {/* Language Toggle */}
        <button onClick={toggleUILanguage} className="px-4 py-2 text-sm font-medium rounded-lg border border-gray-200 text-gray-700 hover:bg-gray-50 transition-colors md:ml-2">
          🌐 हिन्दी
        </button>

        {/* Auth Button */}
        {user ? (
          <button onClick={logout} className="px-4 py-2 text-sm font-bold rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors md:ml-2">
            Log out
          </button>
        ) : (
          <button onClick={onOpenAuth} className="px-4 py-2 text-sm font-bold rounded-lg bg-rti-blue text-white hover:bg-blue-700 shadow-md transition-colors md:ml-2">
            Login / Register
          </button>
        )}

        {/* Bell Icon */}
        <div className="relative">
          <button 
            onClick={() => setIsBellOpen(!isBellOpen)}
            className="w-10 h-10 flex items-center justify-center text-lg rounded-full hover:bg-gray-100 transition-colors relative"
          >
            🔔
            <span className="absolute top-1 right-1 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white hidden"></span>
          </button>
          
          {isBellOpen && (
            <div className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl border border-gray-100 overflow-hidden z-50 animate-fade-in-down">
              <div className="bg-slate-50 px-4 py-3 border-b border-gray-100 font-semibold text-gray-800">
                🔔 Deadline Alerts
              </div>
              <div className="p-6 text-center text-gray-500 text-sm">
                No upcoming deadlines 🎉
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
