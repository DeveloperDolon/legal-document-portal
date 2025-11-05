import React, { useState } from "react";
import { Search, FileText, AlertCircle, Loader2 } from "lucide-react";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    if (!query.trim()) {
      setError("Please enter a search query");
      return;
    }

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: query.trim() }),
      });

      if (!res.ok) {
        throw new Error(`HTTP error! status: ${res.status}`);
      }

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(
        err.message ||
          "Failed to fetch response. Please ensure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !loading) {
      handleSearch();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <div className="container mx-auto px-4 py-8 max-w-5xl">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center gap-3 mb-2">
            <FileText className="w-8 h-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-slate-800">
              Legal Document Search Portal dd
            </h1>
          </div>
          <p className="text-slate-600">
            Search and summarize legal documents with AI assistance
          </p>
        </div>

        {/* Search Form */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <label
            htmlFor="query"
            className="block text-sm font-medium text-slate-700 mb-2"
          >
            Enter your legal query
          </label>
          <div className="flex gap-3">
            <input
              id="query"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="e.g., What are the requirements for forming a contract?"
              className="flex-1 px-4 py-3 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              disabled={loading}
            />
            <button
              onClick={handleSearch}
              disabled={loading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-slate-400 disabled:cursor-not-allowed flex items-center gap-2 font-medium transition-colors"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Searching...
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  Search
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-red-800 mb-1">Error</h3>
              <p className="text-red-700">{error}</p>
            </div>
          </div>
        )}

        {/* Response Display */}
        {response && (
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-xl font-bold text-slate-800 mb-4">
              Search Results
            </h2>

            {/* Summary */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-slate-700 mb-2">
                Summary
              </h3>
              <p className="text-slate-600 leading-relaxed">
                {response.summary}
              </p>
            </div>

            {/* Relevant Documents */}
            <div>
              <h3 className="text-lg font-semibold text-slate-700 mb-3">
                Relevant Documents
              </h3>
              <div className="space-y-4">
                {response.relevant_docs.map((doc, index) => (
                  <div
                    key={index}
                    className="border border-slate-200 rounded-lg p-4 hover:border-blue-300 transition-colors"
                  >
                    <div className="flex items-start gap-3">
                      <FileText className="w-5 h-5 text-blue-600 flex-shrink-0 mt-1" />
                      <div className="flex-1">
                        <h4 className="font-semibold text-slate-800 mb-1">
                          {doc.title}
                        </h4>
                        <p className="text-sm text-slate-600 mb-2">
                          {doc.excerpt}
                        </p>
                        <div className="flex items-center gap-4 text-xs text-slate-500">
                          <span className="bg-blue-50 text-blue-700 px-2 py-1 rounded">
                            Relevance: {(doc.relevance_score * 100).toFixed(0)}%
                          </span>
                          <span>Document ID: {doc.doc_id}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Initial State */}
        {!response && !loading && !error && (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <Search className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-slate-700 mb-2">
              Ready to search
            </h3>
            <p className="text-slate-500">
              Enter a legal query above to get started
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
