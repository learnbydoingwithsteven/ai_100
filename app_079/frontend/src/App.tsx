import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_URL}/api/v1/predict`, {
        data: [1, 2, 3, 4, 5]
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  return (
    <div style={{padding: '20px'}}>
      <h1>AI Application 79</h1>
      <p>AI application</p>
      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Processing...' : 'Predict'}
      </button>
      {result && (
        <div>
          <h3>Result:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
