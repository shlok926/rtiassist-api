import React from 'react';

const FilingGuide = () => {
  return (
    <div className="w-full max-w-4xl mx-auto p-4 md:p-8 animate-fade-in text-left">
      
      {/* Hero */}
      <div className="bg-gradient-to-r from-blue-900 to-rti-blue rounded-2xl p-8 mb-10 text-white shadow-xl text-center">
        <div className="text-5xl mb-4">📖</div>
        <h2 className="text-3xl md:text-4xl font-black mb-3">Visual Filing Guide</h2>
        <p className="text-blue-100 text-lg max-w-2xl mx-auto">
          Step-by-step illustrated guide to file your RTI application successfully.
        </p>
      </div>

      <div className="space-y-8 relative before:absolute before:inset-0 before:ml-5 md:before:mx-auto md:before:translate-x-0 before:h-full before:w-1 before:bg-gradient-to-b before:from-rti-blue before:to-transparent">
        
        {/* Step 1 */}
        <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
          <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-rti-blue text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 font-bold text-lg">
            1
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-6 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
              <span className="text-2xl">🎯</span> Generate Your RTI Draft
            </h3>
            <p className="text-gray-600 mb-4 text-sm">
              Use RTIAssist to generate your legally correct RTI application in your preferred language. The AI will automatically identify the correct department and PIO.
            </p>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start gap-2"><span className="text-green-500">✅</span> Be specific about what information you need</li>
              <li className="flex items-start gap-2"><span className="text-green-500">✅</span> Mention time period and location if relevant</li>
              <li className="flex items-start gap-2"><span className="text-green-500">✅</span> Review the quality score — aim for 70+</li>
            </ul>
          </div>
        </div>

        {/* Step 2 */}
        <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
          <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-rti-blue text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 font-bold text-lg">
            2
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-6 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
              <span className="text-2xl">💰</span> Arrange Application Fee
            </h3>
            <p className="text-gray-600 mb-4 text-sm">
              Most states charge ₹10. Get an Indian Postal Order (IPO) or Court Fee Stamp from your nearest post office or court.
            </p>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start gap-2"><span>💳</span> IPO should be in the name of the concerned department</li>
              <li className="flex items-start gap-2"><span>💳</span> BPL cardholders are exempt — attach BPL card copy</li>
              <li className="flex items-start gap-2"><span>💳</span> Some states accept online payment via portal</li>
            </ul>
          </div>
        </div>

        {/* Step 3 */}
        <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
          <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-rti-blue text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 font-bold text-lg">
            3
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-6 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
              <span className="text-2xl">📝</span> Print & Sign
            </h3>
            <p className="text-gray-600 mb-4 text-sm">
              Print the generated RTI draft on plain paper. Sign at the bottom with your full name and date.
            </p>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start gap-2"><span>🖊️</span> Use black or blue pen for signature</li>
              <li className="flex items-start gap-2"><span>🖊️</span> Make 2 copies — one for submission, one for records</li>
              <li className="flex items-start gap-2"><span>🖊️</span> Attach IPO/stamp or BPL card copy</li>
            </ul>
          </div>
        </div>

        {/* Step 4 */}
        <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
          <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-rti-blue text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 font-bold text-lg">
            4
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-6 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
              <span className="text-2xl">📬</span> Submit Application
            </h3>
            <p className="text-gray-600 mb-4 text-sm">
              Send via registered post or hand-deliver to the PIO office address shown in your generated application.
            </p>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start gap-2"><span>📮</span> Registered Post with Acknowledgement (Track Number)</li>
              <li className="flex items-start gap-2"><span>📮</span> Speed Post (faster, recommended for urgent matters)</li>
              <li className="flex items-start gap-2"><span>📮</span> Hand delivery (get receipt with date stamp)</li>
            </ul>
          </div>
        </div>

        {/* Step 5 */}
        <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group">
          <div className="flex items-center justify-center w-10 h-10 rounded-full border-4 border-white bg-rti-blue text-white shadow shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10 font-bold text-lg">
            5
          </div>
          <div className="w-[calc(100%-4rem)] md:w-[calc(50%-2.5rem)] bg-white p-6 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-shadow">
            <h3 className="text-xl font-bold text-gray-900 mb-2 flex items-center gap-2">
              <span className="text-2xl">⏰</span> Track Deadline
            </h3>
            <p className="text-gray-600 mb-4 text-sm">
              PIO must respond within 30 days (48 hours for life-threatening matters). Use RTIAssist Tracker to monitor.
            </p>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-start gap-2"><span>📱</span> Save tracking number from registered post</li>
              <li className="flex items-start gap-2"><span>📱</span> Add to RTIAssist Tracker with filing date</li>
              <li className="flex items-start gap-2"><span>📱</span> Check mailbox regularly for response</li>
            </ul>
          </div>
        </div>

      </div>

      <div className="mt-16 bg-blue-50 border border-blue-100 rounded-2xl p-8">
        <h3 className="text-2xl font-bold text-blue-900 mb-6 text-center">🤔 Common Questions</h3>
        <div className="space-y-6">
          <div>
            <h4 className="font-bold text-blue-800">❓ Can I file RTI online?</h4>
            <p className="text-blue-900 text-sm mt-1">Yes! Most central government departments accept RTIs via rtionline.gov.in. You can copy your draft there and pay online. However, some state departments still require postal submission.</p>
          </div>
          <div>
            <h4 className="font-bold text-blue-800">❓ Do I need a lawyer?</h4>
            <p className="text-blue-900 text-sm mt-1">No! RTI Act is designed for ordinary citizens. You don't need legal representation. RTIAssist ensures your application is legally correct.</p>
          </div>
          <div>
            <h4 className="font-bold text-blue-800">❓ Can they reject my RTI?</h4>
            <p className="text-blue-900 text-sm mt-1">PIOs can only reject if your query falls under Section 8 exemptions (national security, personal privacy, etc.). Even if rejected, you have the right to appeal.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FilingGuide;
