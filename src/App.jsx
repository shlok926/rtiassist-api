import React, { useState } from 'react';
import { useAuth } from './context/AuthContext';
import AuthModal from './components/auth/AuthModal';
import Navbar from './components/layout/Navbar';
import RTIForm from './components/rti/RTIForm';
import Tracker from './components/tracker/Tracker';
import LegalToolsHub from './components/legal/LegalToolsHub';
import SecondAppeal from './components/legal/SecondAppeal';
import ConsumerCourt from './components/legal/ConsumerCourt';
import LegalNotice from './components/legal/LegalNotice';
import LabourComplaint from './components/legal/LabourComplaint';
import FilingGuide from './components/info/FilingGuide';
import SuccessStories from './components/info/SuccessStories';
import FeesCalculator from './components/info/FeesCalculator';
import About from './components/info/About';
import ExamplesLibrary from './components/info/ExamplesLibrary';
import Settings from './components/info/Settings';
import CaseDetail from './components/case/CaseDetail';

function App() {
  const [activeTab, setActiveTab] = useState('home');
  const [selectedCaseId, setSelectedCaseId] = useState(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const { user, loading } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50 font-sans flex flex-col">
      <Navbar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        onOpenAuth={() => setIsAuthModalOpen(true)}
      />
      <AuthModal isOpen={isAuthModalOpen} onClose={() => setIsAuthModalOpen(false)} />
      
      <main className="flex-grow flex flex-col items-center p-4 md:p-8 space-y-8">
        
        {activeTab === 'home' && (
          <>
            {/* Hero Section */}
            <div className="text-center mt-8 max-w-3xl animate-fade-in">
              <div className="inline-block px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-bold mb-4">
                🇮🇳 Free Forever
              </div>
              <h1 className="text-4xl md:text-5xl font-black text-gray-900 leading-tight mb-4">
                File RTI in <span className="text-rti-blue">Any</span> Indian <span className="text-rti-green">Language</span>
              </h1>
              <p className="text-gray-600 text-lg">
                India's most powerful free AI tool. Advanced multi-layer reasoning. 11 languages, 28 states. Section 8 exemption check. 100% free Forever.
              </p>
            </div>

            {/* The Generator Form */}
            <RTIForm setActiveTab={setActiveTab} setSelectedCaseId={setSelectedCaseId} onOpenAuth={() => setIsAuthModalOpen(true)} />
          </>
        )}

        {activeTab === 'tracker' && <Tracker setActiveTab={setActiveTab} setSelectedCaseId={setSelectedCaseId} />}
        {activeTab === 'case-detail' && <CaseDetail caseId={selectedCaseId} setActiveTab={setActiveTab} />}
        {activeTab === 'legaltools' && <LegalToolsHub setActiveTab={setActiveTab} />}
        {activeTab === 'second-appeal' && <SecondAppeal setActiveTab={setActiveTab} />}
        {activeTab === 'consumer-court' && <ConsumerCourt setActiveTab={setActiveTab} />}
        {activeTab === 'legal-notice' && <LegalNotice setActiveTab={setActiveTab} />}
        {activeTab === 'labour-complaint' && <LabourComplaint setActiveTab={setActiveTab} />}
        
        {activeTab === 'guide' && <FilingGuide />}
        {activeTab === 'stories' && <SuccessStories />}
        {activeTab === 'fees' && <FeesCalculator />}
        {activeTab === 'about' && <About />}
        {activeTab === 'examples' && <ExamplesLibrary setActiveTab={setActiveTab} />}
        {activeTab === 'settings' && <Settings />}

      </main>
      
      {/* Footer */}
      <footer className="w-full bg-white border-t border-gray-200 mt-12 py-8">
        <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="text-gray-500 text-sm font-medium">
            © {new Date().getFullYear()} RTIAssist. Built for India.
          </div>
          <div className="flex gap-6">
            <button onClick={() => setActiveTab('guide')} className="text-sm font-bold text-gray-600 hover:text-rti-blue transition-colors">📖 Filing Guide</button>
            <button onClick={() => setActiveTab('stories')} className="text-sm font-bold text-gray-600 hover:text-rti-blue transition-colors">🌟 Success Stories</button>
            <button onClick={() => setActiveTab('about')} className="text-sm font-bold text-gray-600 hover:text-rti-blue transition-colors">🏛️ About</button>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
