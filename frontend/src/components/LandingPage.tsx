import React, { useState } from 'react';

interface LandingPageProps {
  onValidate: (idea: string) => Promise<void>;
  isLoading?: boolean;
}

export default function LandingPage({ onValidate, isLoading }: LandingPageProps) {
  const [input, setInput] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      await onValidate(input);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 to-indigo-700 flex items-center justify-center p-6">
      <div className="max-w-2xl w-full">
        {/* Logo/Title */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            AI Research Report
          </h1>
          <p className="text-xl text-blue-100">
            Enter any topic and get a comprehensive research report
          </p>
        </div>

        {/* Search Box */}
        <div className="bg-white rounded-lg shadow-2xl p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Research Topic
              </label>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="e.g., AI in healthcare, Machine learning applications..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className={`w-full py-3 px-4 rounded-lg font-bold text-white transition ${
                isLoading || !input.trim()
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 active:scale-95'
              }`}
            >
              {isLoading ? (
                <div className="flex items-center justify-center gap-2">
                  <div className="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></div>
                  Researching...
                </div>
              ) : (
                'Generate Report'
              )}
            </button>
          </form>

          {/* Examples */}
          <div className="mt-8 pt-6 border-t">
            <p className="text-sm font-medium text-gray-700 mb-3">
              Try these topics:
            </p>
            <div className="space-y-2">
              {[
                'Impact of AI on healthcare',
                'Machine learning in finance',
                'Deep learning for computer vision',
                'Natural language processing applications',
              ].map((example) => (
                <button
                  key={example}
                  onClick={() => setInput(example)}
                  disabled={isLoading}
                  className="block w-full text-left px-4 py-2 text-sm text-blue-600 hover:bg-blue-50 rounded transition disabled:opacity-50"
                >
                  → {example}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Footer Info */}
        <div className="mt-12 text-center text-blue-100">
          <p className="text-sm">
            Powered by AI · Searches web + academic papers
          </p>
        </div>
      </div>
    </div>
  );
}