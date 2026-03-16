import { useState } from 'react';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8002';

function App() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<string>('');
  const [analyzing, setAnalyzing] = useState(false);
  const [smiles, setSmiles] = useState<string>('CC(=O)Oc1ccccc1C(=O)O'); // Default Aspirin

  const handlePredict = async () => {
    setLoading(true);
    setAnalysis('');
    try {
      const response = await axios.post(`${API_URL}/api/v1/predict`, {
        smiles: smiles
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  const handleAnalyze = async () => {
    if (!result) return;
    setAnalyzing(true);
    try {
      const response = await axios.post(`${API_URL}/api/v1/analyze`, {
        smiles: smiles,
        prediction: result.prediction,
        confidence: result.confidence
      });
      setAnalysis(response.data.analysis);
    } catch (error) {
      console.error(error);
    }
    setAnalyzing(false);
  };

  return (
    <div style={{ padding: '40px', maxWidth: '800px', margin: '0 auto', fontFamily: 'system-ui, sans-serif' }}>
      <header style={{ marginBottom: '40px', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5rem', color: '#1a1a1a', marginBottom: '10px' }}>💊 Drug Discovery Predictor</h1>
        <p style={{ color: '#666', fontSize: '1.2rem' }}>Molecular property prediction using AI</p>
      </header>

      <div style={{ background: '#f8f9fa', padding: '30px', borderRadius: '12px', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' }}>

        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', marginBottom: '8px', color: '#4b5563', fontWeight: 500 }}>
            Enter Molecule SMILES string:
          </label>
          <input
            type="text"
            value={smiles}
            onChange={(e) => setSmiles(e.target.value)}
            style={{
              width: '100%',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #d1d5db',
              fontFamily: 'monospace',
              marginBottom: '10px'
            }}
            placeholder="e.g. CC(=O)Oc1ccccc1C(=O)O"
          />
        </div>

        <button
          onClick={handlePredict}
          disabled={loading || !smiles}
          style={{
            background: '#0ea5e9',
            color: 'white',
            border: 'none',
            padding: '12px 24px',
            borderRadius: '8px',
            fontSize: '1rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.7 : 1,
            width: '100%',
            fontWeight: 600
          }}
        >
          {loading ? 'Processing...' : 'Run Prediction'}
        </button>

        {result && (
          <div style={{ marginTop: '30px' }}>
            <h3 style={{ color: '#333' }}>Prediction Result:</h3>
            <div style={{ background: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
              <pre style={{ margin: 0, fontSize: '0.9rem', color: '#4b5563' }}>{JSON.stringify(result, null, 2)}</pre>
            </div>

            <div style={{ marginTop: '20px', borderTop: '1px solid #e5e7eb', paddingTop: '20px' }}>
              <button
                onClick={handleAnalyze}
                disabled={analyzing}
                style={{
                  background: '#8b5cf6',
                  color: 'white',
                  border: 'none',
                  padding: '10px 20px',
                  borderRadius: '8px',
                  cursor: analyzing ? 'not-allowed' : 'pointer',
                  opacity: analyzing ? 0.7 : 1,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  fontWeight: 600
                }}
              >
                {analyzing ? 'Analyzer Running...' : '🧪 Generate AI Analysis'}
              </button>

              {analysis && (
                <div style={{ marginTop: '20px', background: '#f3f0ff', padding: '20px', borderRadius: '8px', border: '1px solid #ddd6fe' }}>
                  <h4 style={{ margin: '0 0 10px 0', color: '#5b21b6' }}>AI Assistant Report</h4>
                  <p style={{ margin: 0, lineHeight: 1.6, color: '#4c1d95', whiteSpace: 'pre-wrap' }}>{analysis}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
