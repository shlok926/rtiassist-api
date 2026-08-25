import React, { useState } from 'react';

const LanguageModal = ({ isOpen, onClose, onConfirm }) => {
  const [selectedLang, setSelectedLang] = useState('english');

  if (!isOpen) return null;

  const languages = [
    { code: 'english', label: '🇬🇧 English' },
    { code: 'hindi', label: '🇮🇳 हिंदी' },
    { code: 'marathi', label: 'मराठी' },
    { code: 'tamil', label: 'தமிழ்' },
    { code: 'telugu', label: 'తెలుగు' },
    { code: 'kannada', label: 'ಕನ್ನಡ' },
    { code: 'bengali', label: 'বাংলা' },
    { code: 'gujarati', label: 'ગુજરાતી' },
    { code: 'punjabi', label: 'ਪੰਜਾਬੀ' },
    { code: 'malayalam', label: 'മലയാളം' },
    { code: 'odia', label: 'ଓଡ଼ିଆ' }
  ];

  const handleConfirm = () => {
    onConfirm(selectedLang);
  };

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/60 backdrop-blur-sm p-4 animate-fade-in" onClick={onClose}>
      <div 
        className="bg-white rounded-2xl shadow-2xl w-full max-w-lg overflow-hidden flex flex-col transform transition-all scale-100"
        onClick={e => e.stopPropagation()}
      >
        <div className="p-6 md:p-8">
          <div className="text-center mb-6">
            <h3 className="text-2xl font-black text-gray-900 mb-2">🌐 Draft Language / ड्राफ्ट की भाषा चुनें</h3>
            <p className="text-gray-500">Your problem is understood. Now choose the language for your RTI draft.</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-8">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => setSelectedLang(lang.code)}
                className={`py-3 px-2 rounded-xl text-sm font-bold transition-all border-2
                  ${selectedLang === lang.code 
                    ? 'border-rti-blue bg-blue-50 text-rti-blue shadow-md' 
                    : 'border-gray-100 bg-white text-gray-700 hover:border-gray-200 hover:bg-gray-50'
                  }`}
              >
                {lang.label}
              </button>
            ))}
          </div>

          <div className="flex gap-4">
            <button 
              onClick={onClose}
              className="flex-1 py-3 px-4 font-bold text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-xl transition-colors"
            >
              ← Back
            </button>
            <button 
              onClick={handleConfirm}
              className="flex-[2] py-3 px-4 font-bold text-white bg-gradient-to-r from-rti-blue to-blue-700 hover:from-blue-700 hover:to-blue-800 rounded-xl shadow-lg transition-transform hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-2"
            >
              ⚡ Generate RTI Draft
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LanguageModal;
