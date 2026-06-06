import { useState, useEffect } from 'react';
import LandingPage from './components/LandingPage';
import ResultsPage from './components/ResultsPage';
import { ValidationResult } from './types/validation';
import { fetchValidationResult } from './api/validationApi';

const STORAGE_KEY = 'validationAppState';

function App() {
  const [showResults, setShowResults] = useState(false);
  const [validationData, setValidationData] = useState<ValidationResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isRestoring, setIsRestoring] = useState(true);
  const [isValidating, setIsValidating] = useState(false);

  // ✅ Restore state on app load
  useEffect(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        if (parsed.validationData) {
          setValidationData(parsed.validationData);
          setShowResults(true);
        }
        if (parsed.error) {
          setError(parsed.error);
        }
      }
    } catch (e) {
      console.error('Failed to restore saved state', e);
      localStorage.removeItem(STORAGE_KEY);
    } finally {
      setIsRestoring(false);
    }
  }, []);

  // ✅ Save state to localStorage
  useEffect(() => {
    if (showResults && validationData) {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ validationData, error })
      );
    }
  }, [showResults, validationData, error]);

  const handleValidate = async (idea: string) => {
    setIsValidating(true);
    setError(null);
    setValidationData(null);

    try {
      const result = await fetchValidationResult(idea);
      setValidationData(result);
      setShowResults(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Unknown error';
      setError(`❌ Failed to validate: ${errorMsg}`);
      setShowResults(false);
    } finally {
      setIsValidating(false);
    }
  };

  const handleBack = () => {
    setShowResults(false);
    setValidationData(null);
    setError(null);
    localStorage.removeItem(STORAGE_KEY);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (isRestoring) {
    return (
      <div className="min-h-screen flex items-center justify-center text-gray-600 text-lg">
        Restoring your session...
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {showResults && validationData ? (
        <ResultsPage
          data={validationData}
          onBack={handleBack}
          error={error}
          isLoading={isValidating}
        />
      ) : (
        <LandingPage 
          onValidate={handleValidate}
          isLoading={isValidating}
        />
      )}
    </div>
  );
}

export default App;