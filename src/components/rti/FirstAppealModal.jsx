import React from 'react';

const FirstAppealModal = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  const draft = `BEFORE THE FIRST APPELLATE AUTHORITY
Under Section 19(1) of the RTI Act, 2005

Subject: First Appeal under Section 19(1) of RTI Act 2005

Sir/Madam,
I had filed an RTI application on __________. 
However, I have not received any satisfactory response from the PIO within the mandated 30 days.

Therefore, I am filing this First Appeal. I request you to direct the PIO to provide the complete information free of cost under Section 7(6) of the RTI Act.

Enclosed: 
1. Copy of original RTI Application
2. Proof of dispatch/receipt

Yours faithfully,
Signature: ___________
Name: ___________
Date: ${new Date().toISOString().split('T')[0]}`;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center bg-gray-900/60 backdrop-blur-sm p-4 animate-fade-in" onClick={onClose}>
      <div 
        className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col transform transition-all scale-100 max-h-[90vh]"
        onClick={e => e.stopPropagation()}
      >
        <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
          <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <span>📝</span> First Appeal Letter
          </h3>
          <button 
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 hover:bg-gray-200 p-1 rounded-lg transition-colors"
          >
            ✕
          </button>
        </div>
        
        <div className="p-6 overflow-y-auto">
          <p className="text-sm text-gray-600 mb-4 bg-blue-50 p-3 rounded-lg border border-blue-100">
            <strong>When to use:</strong> File this if the PIO does not respond within 30 days (or gives an unsatisfactory response). Send to the First Appellate Authority under Section 19(1) of RTI Act 2005.
          </p>
          
          <div className="bg-white border border-gray-200 p-4 rounded-xl font-mono text-sm text-gray-800 whitespace-pre-wrap">
            {draft}
          </div>
        </div>

        <div className="p-6 border-t border-gray-100 bg-gray-50 flex gap-4">
          <button 
            onClick={() => navigator.clipboard.writeText(draft)}
            className="flex-1 py-3 px-4 font-bold text-gray-700 bg-white border border-gray-200 hover:bg-gray-50 rounded-xl transition-colors shadow-sm flex items-center justify-center gap-2"
          >
            📋 Copy Appeal
          </button>
          <button 
            onClick={onClose}
            className="flex-1 py-3 px-4 font-bold text-white bg-rti-blue hover:bg-blue-700 rounded-xl shadow-lg transition-colors"
          >
            Done
          </button>
        </div>
      </div>
    </div>
  );
};

export default FirstAppealModal;
