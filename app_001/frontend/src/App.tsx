import { useState } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js';
import { Pie, Bar } from 'react-chartjs-2';
import './App.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface PredictionResult {
  prediction: string;
  confidence: number;
  probabilities: { [key: string]: number };
  processing_time: number;
  timestamp: string;
}

interface Metrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: number[][];
}

function App() {
  const [inputData, setInputData] = useState<string>('');
  const [age, setAge] = useState<string>('');
  const [gender, setGender] = useState<string>('Male');
  const [symptoms, setSymptoms] = useState<string>('');
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [analysis, setAnalysis] = useState<string>('');
  const [analyzing, setAnalyzing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handlePredict = async () => {
    try {
      setLoading(true);
      setError('');
      setAnalysis('');

      const data = inputData.split(',').map(x => parseFloat(x.trim()));

      const response = await axios.post(`${API_URL}/api/v1/predict`, {
        data,
        confidence_threshold: 0.5
      });

      setPrediction(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Prediction failed');
    } finally {
      setLoading(false);
    }
  };

  const loadMetrics = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/metrics`);
      setMetrics(response.data);
    } catch (err: any) {
      setError('Failed to load metrics');
    }
  };

  const handleAnalyze = async () => {
    if (!prediction) return;
    try {
      setAnalyzing(true);
      const response = await axios.post(`${API_URL}/api/v1/analyze`, {
        prediction: prediction.prediction,
        confidence: prediction.confidence,
        probabilities: prediction.probabilities,
        patient_data: { age, gender, symptoms }
      });

      setAnalysis(response.data.analysis);
    } catch (err) {
      setError('Analysis failed');
    } finally {
      setAnalyzing(false);
    }
  };

  const pieData = prediction ? {
    labels: Object.keys(prediction.probabilities),
    datasets: [{
      data: Object.values(prediction.probabilities),
      backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
    }]
  } : null;

  const barData = metrics ? {
    labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
    datasets: [{
      label: 'Model Performance',
      data: [metrics.accuracy, metrics.precision, metrics.recall, metrics.f1_score],
      backgroundColor: '#3b82f6',
    }]
  } : null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-800 mb-4">
            🏥 Medical Image Diagnosis
          </h1>
          <p className="text-xl text-gray-600">
            AI-Powered Medical Image Analysis System
          </p>
        </header>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Prediction Panel */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <h2 className="text-2xl font-bold mb-6 text-gray-800">
              Make Prediction
            </h2>

            <h2 className="text-2xl font-bold mb-6 text-gray-800">
              Patient Data
            </h2>

            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Age</label>
                <input
                  type="number"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  placeholder="e.g. 45"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Gender</label>
                <select
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                >
                  <option>Male</option>
                  <option>Female</option>
                  <option>Other</option>
                </select>
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">Symptoms</label>
              <textarea
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                placeholder="Describe symptoms..."
                rows={2}
              />
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Image Features (Simulated)
              </label>
              <textarea
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={4}
                value={inputData}
                onChange={(e) => setInputData(e.target.value)}
                placeholder="1.5, 2.3, 4.1, 3.2, ..."
              />
            </div>

            <button
              onClick={handlePredict}
              disabled={loading || !inputData}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Processing...' : 'Predict'}
            </button>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                {error}
              </div>
            )}

            {prediction && (
              <div className="mt-6 p-6 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg">
                <h3 className="text-xl font-bold mb-4">Prediction Result</h3>
                <div className="space-y-2">
                  <p className="text-lg">
                    <span className="font-semibold">Diagnosis:</span>{' '}
                    <span className={`font-bold ${prediction.prediction === 'Normal' ? 'text-green-600' :
                      prediction.prediction === 'Abnormal' ? 'text-yellow-600' :
                        'text-red-600'
                      }`}>
                      {prediction.prediction}
                    </span>
                  </p>
                  <p>
                    <span className="font-semibold">Confidence:</span>{' '}
                    {(prediction.confidence * 100).toFixed(2)}%
                  </p>
                  <p>
                    <span className="font-semibold">Processing Time:</span>{' '}
                    {prediction.processing_time.toFixed(3)}s
                  </p>
                </div>

                {pieData && (
                  <div className="mt-6">
                    <h4 className="font-semibold mb-2">Probability Distribution</h4>
                    <div className="w-64 mx-auto">
                      <Pie data={pieData} />
                    </div>
                  </div>
                )}
              </div>
            )}


            {prediction && (
              <div className="mt-6 pt-6 border-t border-gray-100">
                <button
                  onClick={handleAnalyze}
                  disabled={analyzing}
                  className="w-full bg-purple-600 hover:bg-purple-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200 disabled:opacity-50"
                >
                  {analyzing ? 'Generating Consultant Report...' : '🔍 Generate AI Report'}
                </button>

                {analysis && (
                  <div className="mt-4 p-4 bg-purple-50 rounded-lg border border-purple-100">
                    <h4 className="font-bold text-purple-900 mb-2">AI Consultant Report</h4>
                    <p className="text-gray-800 text-sm leading-relaxed whitespace-pre-wrap">
                      {analysis}
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Metrics Panel */}
          <div className="bg-white rounded-2xl shadow-xl p-8">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-gray-800">
                Model Performance
              </h2>
              <button
                onClick={loadMetrics}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-2 px-4 rounded-lg transition duration-200"
              >
                Load Metrics
              </button>
            </div>

            {metrics && (
              <div>
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="p-4 bg-blue-50 rounded-lg">
                    <p className="text-sm text-gray-600">Accuracy</p>
                    <p className="text-2xl font-bold text-blue-600">
                      {(metrics.accuracy * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <p className="text-sm text-gray-600">Precision</p>
                    <p className="text-2xl font-bold text-green-600">
                      {(metrics.precision * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div className="p-4 bg-yellow-50 rounded-lg">
                    <p className="text-sm text-gray-600">Recall</p>
                    <p className="text-2xl font-bold text-yellow-600">
                      {(metrics.recall * 100).toFixed(1)}%
                    </p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg">
                    <p className="text-sm text-gray-600">F1 Score</p>
                    <p className="text-2xl font-bold text-purple-600">
                      {(metrics.f1_score * 100).toFixed(1)}%
                    </p>
                  </div>
                </div>

                {barData && (
                  <div className="mb-6">
                    <h4 className="font-semibold mb-2">Performance Metrics</h4>
                    <Bar data={barData} options={{ scales: { y: { beginAtZero: true, max: 1 } } }} />
                  </div>
                )}

                <div>
                  <h4 className="font-semibold mb-2">Confusion Matrix</h4>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="bg-gray-100">
                          <th className="p-2 border">Actual \ Predicted</th>
                          <th className="p-2 border">Normal</th>
                          <th className="p-2 border">Abnormal</th>
                          <th className="p-2 border">Critical</th>
                        </tr>
                      </thead>
                      <tbody>
                        {metrics.confusion_matrix.map((row, i) => (
                          <tr key={i}>
                            <td className="p-2 border font-semibold bg-gray-50">
                              {['Normal', 'Abnormal', 'Critical'][i]}
                            </td>
                            {row.map((val, j) => (
                              <td key={j} className={`p-2 border text-center ${i === j ? 'bg-green-100 font-bold' : ''}`}>
                                {val}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        <footer className="mt-12 text-center text-gray-600">
          <p>Medical Image Diagnosis System v1.0.0</p>
          <p className="text-sm">Powered by FastAPI + React + AI/ML</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
