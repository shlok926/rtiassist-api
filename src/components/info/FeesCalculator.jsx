import React, { useState } from 'react';

const FeesCalculator = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const feesData = [
    {state:'Central Government',fee:'₹10',modes:'IPO, DD, Court Fee Stamp, Online (Debit/Credit/UPI)',days:30,portal:'https://rtionline.gov.in'},
    {state:'Andhra Pradesh',fee:'₹10',modes:'Court Fee Stamp, DD, IPO',days:30,portal:'https://rtionline.gov.in'},
    {state:'Assam',fee:'₹10',modes:'Court Fee Stamp, IPO',days:30,portal:'https://rtionline.gov.in'},
    {state:'Bihar',fee:'₹10',modes:'Court Fee Stamp, IPO, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Chhattisgarh',fee:'₹10',modes:'Court Fee Stamp, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Delhi',fee:'₹10',modes:'IPO, Court Fee Stamp, Online',days:30,portal:'https://rti.delhi.gov.in'},
    {state:'Goa',fee:'₹10',modes:'Court Fee Stamp, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Gujarat',fee:'₹20',modes:'Court Fee Stamp, DD, Online',days:30,portal:'https://rtionline.gov.in'},
    {state:'Haryana',fee:'₹10',modes:'Court Fee Stamp, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Himachal Pradesh',fee:'₹10',modes:'Court Fee Stamp, IPO',days:30,portal:'https://rtionline.gov.in'},
    {state:'Jharkhand',fee:'₹10',modes:'Court Fee Stamp, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Karnataka',fee:'₹10',modes:'Court Fee Stamp, DD, Online',days:30,portal:'https://rtionline.gov.in'},
    {state:'Kerala',fee:'₹10',modes:'Court Fee Stamp, Online',days:30,portal:'https://rtiportal.kerala.gov.in'},
    {state:'Madhya Pradesh',fee:'₹10',modes:'Court Fee Stamp, IPO, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Maharashtra',fee:'₹10',modes:'Court Fee Stamp, DD, Online',days:30,portal:'https://rtionline.gov.in'},
    {state:'Manipur',fee:'₹10',modes:'Court Fee Stamp',days:30,portal:'https://rtionline.gov.in'},
    {state:'Meghalaya',fee:'₹10',modes:'Court Fee Stamp, IPO',days:30,portal:'https://rtionline.gov.in'},
    {state:'Odisha',fee:'₹10',modes:'Court Fee Stamp, IPO',days:30,portal:'https://rtionline.gov.in'},
    {state:'Punjab',fee:'₹10',modes:'Court Fee Stamp, IPO, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Rajasthan',fee:'₹10',modes:'Court Fee Stamp, IPO, Online',days:30,portal:'https://rtionline.gov.in'},
    {state:'Sikkim',fee:'₹10',modes:'Court Fee Stamp',days:30,portal:'https://rtionline.gov.in'},
    {state:'Tamil Nadu',fee:'₹10',modes:'Court Fee Stamp, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Telangana',fee:'₹10',modes:'Court Fee Stamp, DD',days:30,portal:'https://rtionline.gov.in'},
    {state:'Uttar Pradesh',fee:'₹10',modes:'Treasury Challan, IPO, Online',days:30,portal:'https://rtionline.up.gov.in'},
    {state:'Uttarakhand',fee:'₹10',modes:'Court Fee Stamp, IPO',days:30,portal:'https://rtionline.gov.in'},
    {state:'West Bengal',fee:'₹10',modes:'Court Fee Stamp, IPO, DD',days:30,portal:'https://rtionline.gov.in'},
  ];

  const filteredFees = feesData.filter(f => f.state.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <div className="w-full max-w-6xl mx-auto p-4 md:p-8 animate-fade-in text-left">
      
      {/* Hero */}
      <div className="text-center mb-8">
        <div className="text-5xl mb-4">💰</div>
        <h2 className="text-3xl md:text-4xl font-black text-gray-900 mb-4">RTI Fee Calculator</h2>
        <p className="text-gray-600 text-lg max-w-2xl mx-auto">
          State-wise filing fees, payment modes, and portal links. BPL applicants are always exempt from fees.
        </p>
      </div>

      <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-xl p-4 mb-8 text-center font-medium shadow-sm">
        <span className="text-xl mr-2">✅</span> <strong>BPL (Below Poverty Line) applicants</strong> — Zero fee across all states. Attach a copy of your BPL card with the application.
      </div>

      <div className="max-w-md mx-auto mb-8">
        <input 
          type="text" 
          placeholder="🔍 Search your state..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full p-4 rounded-xl border border-gray-300 shadow-sm focus:ring-2 focus:ring-rti-blue focus:outline-none"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredFees.map((f, idx) => (
          <div key={idx} className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100 hover:-translate-y-1 transition-transform flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-bold text-gray-900">{f.state}</h3>
                <span className="px-3 py-1 bg-green-100 text-green-800 font-black rounded-full text-lg">{f.fee}</span>
              </div>
              
              <div className="space-y-2 mb-6">
                <p className="text-sm text-gray-700">
                  <strong className="text-gray-900">📋 Payment Modes:</strong><br/>
                  {f.modes}
                </p>
                <p className="text-sm text-gray-700">
                  <strong className="text-gray-900">⏱ Response Time:</strong><br/>
                  {f.days} days
                </p>
              </div>
            </div>
            
            <a 
              href={f.portal} 
              target="_blank" 
              rel="noopener noreferrer"
              className="block w-full text-center px-4 py-3 bg-gray-50 hover:bg-gray-100 text-rti-blue font-bold rounded-xl border border-gray-200 transition-colors"
            >
              File RTI Online →
            </a>
          </div>
        ))}
      </div>

      {filteredFees.length === 0 && (
        <div className="text-center text-gray-500 py-10">
          No states found matching "{searchTerm}"
        </div>
      )}

    </div>
  );
};

export default FeesCalculator;
