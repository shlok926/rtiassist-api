import React, { useState, useEffect } from 'react';
import { apiFetch } from '../../utils/api';
import FirstAppealModal from '../rti/FirstAppealModal';

const CaseDetail = ({ caseId, setActiveTab }) => {
  const [caseData, setCaseData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isAppealModalOpen, setIsAppealModalOpen] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [fileToUpload, setFileToUpload] = useState(null);

  const fetchCase = async () => {
    setLoading(true);
    try {
      const res = await apiFetch(`/cases/${caseId}`);
      if (!res.ok) throw new Error('Failed to load case');
      const data = await res.json();
      setCaseData(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (caseId) fetchCase();
  }, [caseId]);

  if (loading) return <div className="p-8 text-center text-gray-500">Loading Case...</div>;
  if (error) return <div className="p-8 text-center text-red-500">Error: {error}</div>;
  if (!caseData) return null;

  const handleConfirmFacts = async () => {
    try {
      await apiFetch(`/cases/${caseId}`, {
        method: 'PATCH',
        body: JSON.stringify({ facts_confirmed: "true" })
      });
      fetchCase();
    } catch (err) {
      alert("Error confirming facts");
    }
  };

  const handleConfirmAction = async (action) => {
    try {
      await apiFetch(`/cases/${caseId}/confirm-action`, {
        method: 'POST',
        body: JSON.stringify({ action })
      });
      fetchCase();
    } catch (err) {
      alert("Error confirming action");
    }
  };

  const handleResolveAuthority = async () => {
    try {
      await apiFetch(`/cases/${caseId}/resolve-authority`, {
        method: 'POST'
      });
      fetchCase();
    } catch (err) {
      alert("Error resolving authority");
    }
  };

  const handleGenerateDocument = async () => {
    setIsGenerating(true);
    try {
      await apiFetch(`/cases/${caseId}/generate-document`, {
        method: 'POST',
        body: JSON.stringify({ language: 'english' })
      });
      fetchCase();
    } catch (err) {
      alert("Error generating document");
    } finally {
      setIsGenerating(false);
    }
  };

  const handleFileCase = async () => {
    try {
      await apiFetch(`/cases/${caseId}/file`, {
        method: 'POST',
        body: JSON.stringify({
          filing_date: new Date().toISOString().split('T')[0],
          filing_method: 'ONLINE'
        })
      });
      fetchCase();
    } catch (err) {
      alert("Error filing case");
    }
  };

  const handleUploadResponse = async () => {
    if (!fileToUpload) return alert('Please select a file');
    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', fileToUpload);
    try {
      await apiFetch(`/cases/${caseId}/responses`, {
        method: 'POST',
        body: formData,
        headers: {} // Need to let browser set Content-Type for FormData
      });
      fetchCase();
    } catch (err) {
      alert("Error uploading response");
    } finally {
      setIsUploading(false);
    }
  };

  const getCitizenStatus = (status) => {
    const map = {
      UNDERSTANDING: "Understanding your problem",
      ACTION_RECOMMENDED: "Action recommended",
      ACTION_CONFIRMED: "Next step confirmed",
      AUTHORITY_RESOLVED: "Receiving authority identified",
      AUTHORITY_REVIEW_REQUIRED: "Authority needs review",
      READY_TO_FILE: "Ready to file",
      FILED: "Filed",
      AWAITING_RESPONSE: "Waiting for government response",
      RESPONSE_RECEIVED: "Response received",
      ANALYSIS_READY: "Response analyzed",
      APPEAL_RECOMMENDED: "First appeal recommended",
      APPEAL_CONFIRMED: "First appeal confirmed",
      CLOSED: "Closed"
    };
    return map[status] || status;
  };

  const facts = caseData.extracted_facts ? JSON.parse(caseData.extracted_facts) : null;

  return (
    <div className="w-full max-w-4xl mx-auto p-4 md:p-8 animate-fade-in space-y-6">
      <button onClick={() => setActiveTab('tracker')} className="text-rti-blue font-semibold mb-4">← Back to Tracker</button>
      
      {/* HEADER */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex flex-col md:flex-row justify-between items-start md:items-center">
        <div>
          <h2 className="text-2xl font-black text-gray-900">{caseData.title || "Case Detail"}</h2>
          <div className="text-gray-500 mt-1">Status: <span className="font-bold text-gray-800">{getCitizenStatus(caseData.status)}</span></div>
        </div>
        <div className="text-sm text-gray-400 mt-4 md:mt-0">
          Created: {new Date(caseData.created_at).toLocaleDateString()}
        </div>
      </div>

      {/* PROBLEM */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-lg font-bold text-gray-900 mb-2">Your Problem</h3>
        <p className="text-gray-700 whitespace-pre-wrap">{caseData.problem_description}</p>
      </div>

      {/* WHAT WE UNDERSTOOD (FACTS) */}
      {caseData.case_objective && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Here's what we understood</h3>
          <div className="space-y-3 mb-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-2 py-2 border-b border-gray-100">
              <div className="text-gray-500 text-sm font-medium">Your goal</div>
              <div className="md:col-span-2 text-gray-800 font-medium">{caseData.case_objective}</div>
            </div>
            {facts && Object.entries(facts).map(([key, val]) => (
              <div key={key} className="grid grid-cols-1 md:grid-cols-3 gap-2 py-2 border-b border-gray-100">
                <div className="text-gray-500 text-sm font-medium capitalize">{key.replace(/_/g, ' ')}</div>
                <div className="md:col-span-2 text-gray-800 font-medium">{Array.isArray(val) ? val.join(', ') : val}</div>
              </div>
            ))}
          </div>
          {caseData.facts_confirmed !== "true" && (
            <div className="flex gap-4">
              <button onClick={handleConfirmFacts} className="px-4 py-2 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 transition">
                Confirm Understanding
              </button>
            </div>
          )}
          {caseData.facts_confirmed === "true" && (
            <div className="text-sm font-bold text-green-600">✓ Facts Confirmed</div>
          )}
        </div>
      )}

      {/* CLARIFICATION */}
      {caseData.recommended_action === "NEEDS_CLARIFICATION" && (
        <div className="bg-yellow-50 p-6 rounded-xl shadow-sm border border-yellow-200">
          <h3 className="text-lg font-bold text-yellow-900 mb-2">Before we continue, we need a little more information.</h3>
          <p className="text-yellow-800 mb-4">Please update your problem description with more details.</p>
          <button onClick={() => alert('Editing description would go here')} className="px-4 py-2 bg-yellow-600 text-white font-bold rounded-lg hover:bg-yellow-700 transition">
            Provide More Information
          </button>
        </div>
      )}

      {/* ACTION RECOMMENDATION */}
      {caseData.recommended_action && caseData.recommended_action !== "NEEDS_CLARIFICATION" && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Based on what you told us</h3>
          <div className="mb-4">
            <div className="text-sm text-gray-500 mb-1">Recommended next step:</div>
            <div className="text-xl font-bold text-rti-blue">{caseData.recommended_action.replace(/_/g, ' ')}</div>
          </div>
          {caseData.status === "ACTION_RECOMMENDED" && (
            <div className="flex gap-4">
              <button onClick={() => handleConfirmAction(caseData.recommended_action)} className="px-4 py-2 bg-rti-blue text-white font-bold rounded-lg hover:bg-blue-700 transition">
                Confirm Action
              </button>
            </div>
          )}
          {['ACTION_CONFIRMED', 'AUTHORITY_RESOLVED', 'READY_TO_FILE', 'FILED', 'RESPONSE_RECEIVED', 'ANALYSIS_READY', 'APPEAL_RECOMMENDED', 'CLOSED'].includes(caseData.status) && (
            <div className="text-sm font-bold text-green-600 mt-2">✓ Action Confirmed</div>
          )}
        </div>
      )}

      {/* AUTHORITY RESOLUTION */}
      {caseData.status === "ACTION_CONFIRMED" && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 text-center">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Next, we need to find the correct authority.</h3>
          <button onClick={handleResolveAuthority} className="px-4 py-2 bg-rti-blue text-white font-bold rounded-lg hover:bg-blue-700 transition">
            Identify Receiving Authority
          </button>
        </div>
      )}

      {/* VERIFIED AUTHORITY */}
      {caseData.authority_id && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Where your request should go</h3>
          <div className="text-sm font-bold text-green-600 mb-2">✓ Verified Authority</div>
          {/* Note: We would fetch Authority Details from /authorities/{id} if needed, but keeping it simple */}
          <div className="text-sm text-gray-600">Authority ID: {caseData.authority_id}</div>
          
          {caseData.status === "AUTHORITY_RESOLVED" && (
            <button onClick={handleGenerateDocument} disabled={isGenerating} className="mt-4 px-4 py-2 bg-rti-blue text-white font-bold rounded-lg hover:bg-blue-700 transition">
              {isGenerating ? "Preparing..." : "Prepare Document"}
            </button>
          )}
        </div>
      )}
      
      {/* AUTHORITY REVIEW REQUIRED */}
      {caseData.status === "AUTHORITY_REVIEW_REQUIRED" && (
        <div className="bg-yellow-50 p-6 rounded-xl shadow-sm border border-yellow-200">
          <h3 className="text-lg font-bold text-yellow-900 mb-2">This authority needs verification before we can safely prepare your document.</h3>
          <p className="text-yellow-800">Our system found multiple or low-confidence matches.</p>
        </div>
      )}

      {/* DOCUMENT */}
      {caseData.documents && caseData.documents.length > 0 && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Your Document is Ready</h3>
          {caseData.documents.map(doc => (
            <div key={doc.id} className="flex justify-between items-center border-b border-gray-100 py-3 last:border-0">
              <div>
                <div className="font-bold text-gray-800">{doc.document_type} (Version {doc.version || 1})</div>
                <div className="text-xs text-gray-500">Created: {new Date(doc.created_at).toLocaleString()}</div>
              </div>
              <div className="flex gap-2">
                <a href={`${window.location.origin}/cases/${caseId}/documents/${doc.id}/pdf`} target="_blank" rel="noreferrer" className="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200">
                  📄 PDF
                </a>
              </div>
            </div>
          ))}

          {caseData.status === "READY_TO_FILE" && (
            <div className="mt-6 pt-6 border-t border-gray-100">
              <h4 className="font-bold text-gray-900 mb-2">File Your Request</h4>
              <p className="text-sm text-gray-600 mb-4">Once you have filed this document online or via post, let us know.</p>
              <button onClick={handleFileCase} className="px-4 py-2 bg-green-600 text-white font-bold rounded-lg hover:bg-green-700 transition">
                Mark as Filed
              </button>
            </div>
          )}
        </div>
      )}

      {/* FILING & TIMELINE */}
      {['FILED', 'RESPONSE_RECEIVED', 'ANALYSIS_READY', 'APPEAL_RECOMMENDED'].includes(caseData.status) && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Timeline</h3>
          {caseData.filing_date && (
            <div className="text-sm text-gray-800 mb-1">Filed on: <span className="font-bold">{caseData.filing_date}</span></div>
          )}
          {caseData.next_deadline && (
            <div className="text-sm text-gray-800 mb-4">
              Expected Response: <span className="font-bold">{caseData.next_deadline}</span>
              {caseData.overdue ? <span className="text-red-500 ml-2 font-bold">({Math.abs(caseData.remaining_days)} days overdue)</span> : <span className="text-orange-500 ml-2 font-bold">({caseData.remaining_days} days remaining)</span>}
            </div>
          )}

          {caseData.status === "FILED" && (
            <div className="mt-6 pt-6 border-t border-gray-100">
              <h4 className="font-bold text-gray-900 mb-2">Have you received a response?</h4>
              <p className="text-sm text-gray-600 mb-4">Upload the government response PDF to analyze it.</p>
              <div className="flex items-center gap-4">
                <input type="file" accept=".pdf" onChange={(e) => setFileToUpload(e.target.files[0])} className="text-sm" />
                <button onClick={handleUploadResponse} disabled={isUploading} className="px-4 py-2 bg-rti-blue text-white font-bold rounded-lg hover:bg-blue-700 transition">
                  {isUploading ? "Uploading..." : "Upload & Analyze"}
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* RESPONSE ANALYSIS */}
      {caseData.response_analyses && caseData.response_analyses.length > 0 && (
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <h3 className="text-lg font-bold text-gray-900 mb-4">Response Analysis</h3>
          {caseData.response_analyses.map((analysis) => (
            <div key={analysis.id} className="space-y-6">
              <div className="bg-gray-50 p-4 rounded-lg">
                <div className="font-bold text-gray-800 mb-2">Summary</div>
                <div className="text-sm text-gray-700">Answered: {analysis.answered.length}</div>
                <div className="text-sm text-gray-700">Not Answered: {analysis.not_answered.length}</div>
              </div>
              
              {analysis.request_mapping && analysis.request_mapping.length > 0 && (
                <div className="space-y-4 mt-4">
                  <h4 className="font-bold text-gray-800">Request Mapping</h4>
                  {analysis.request_mapping.map((mapping, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-lg p-4">
                      <div className="text-sm font-bold text-gray-900 mb-2">Your request #{idx + 1}</div>
                      <p className="text-sm text-gray-700 mb-2 bg-gray-50 p-2 rounded">{mapping.request_text}</p>
                      
                      <div className={`text-xs font-bold px-2 py-1 inline-block rounded mb-2 ${mapping.status === 'Answered' ? 'bg-green-100 text-green-800' : mapping.status === 'Partially answered' ? 'bg-yellow-100 text-yellow-800' : 'bg-red-100 text-red-800'}`}>
                        Status: {mapping.status}
                      </div>

                      {mapping.evidence_excerpt && (
                        <div className="text-sm text-gray-600 bg-blue-50 p-2 rounded mt-2">
                          <span className="font-bold text-rti-blue">Evidence (Page {mapping.page_number || 'Unknown'}):</span> {mapping.evidence_excerpt}
                          {mapping.is_ocr_derived && <span className="ml-2 text-xs text-orange-500 font-bold">(OCR Derived)</span>}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {/* NEXT ACTION RECOMMENDATION */}
              <div className="mt-6 border-t border-gray-100 pt-6">
                <h4 className="font-bold text-gray-800 mb-2">Recommended Next Step</h4>
                <div className="text-lg font-bold text-rti-blue mb-2">{analysis.recommended_action.replace(/_/g, ' ')}</div>
                {analysis.recommended_action === 'FIRST_APPEAL' && caseData.status === 'ANALYSIS_READY' && (
                  <button onClick={() => setIsAppealModalOpen(true)} className="px-4 py-2 bg-rti-blue text-white font-bold rounded-lg hover:bg-blue-700 transition">
                    Start First Appeal
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
      
      <FirstAppealModal isOpen={isAppealModalOpen} onClose={() => setIsAppealModalOpen(false)} />
    </div>
  );
};

export default CaseDetail;
