import { useState } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8003';

interface PatientData {
  age: number;
  gender: string;
  chronic_conditions: string[];
  recent_admissions: number;
}

interface PredictionResult {
  risk_level: string;
  confidence: number;
  probability_distribution: Record<string, number>;
}

function App() {
  const [patient, setPatient] = useState<PatientData>({
    age: 65,
    gender: 'Male',
    chronic_conditions: ['Hypertension'],
    recent_admissions: 1
  });

  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [analysis, setAnalysis] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  // Helper for checkbox handling
  const handleConditionChange = (condition: string) => {
    setPatient(prev => {
      const exists = prev.chronic_conditions.includes(condition);
      return {
        ...prev,
        chronic_conditions: exists
          ? prev.chronic_conditions.filter(c => c !== condition)
          : [...prev.chronic_conditions, condition]
      };
    });
  };

  const handlePredict = async () => {
    setLoading(true);
    setAnalysis('');
    setPrediction(null);
    try {
      const response = await axios.post(`${API_URL}/api/v1/predict`, patient);
      setPrediction(response.data);
    } catch (err) {
      console.error(err);
      alert('Prediction failed. Is backend running on port 8003?');
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!prediction) return;
    setAnalyzing(true);
    try {
      const response = await axios.post(`${API_URL}/api/v1/analyze`, {
        patient_data: patient,
        prediction: prediction.risk_level,
        confidence: prediction.confidence
      });
      setAnalysis(response.data.analysis);
    } catch (err) {
      console.error(err);
      alert('Analysis failed.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-4 sm:px-6 lg:px-8 font-sans text-gray-800">
      <div className="max-w-5xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-extrabold text-blue-900 tracking-tight sm:text-5xl mb-2">
            🏥 Patient Risk Stratification
          </h1>
          <p className="text-xl text-gray-600">AI-Powered Hospital Readmission Prediction</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="bg-blue-600 p-4">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                📋 Patient Profile
              </h2>
            </div>
            <div className="p-6 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                  <input
                    type="number"
                    value={patient.age}
                    onChange={e => setPatient({ ...patient, age: parseInt(e.target.value) || 0 })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                  <select
                    value={patient.gender}
                    onChange={e => setPatient({ ...patient, gender: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  >
                    <option>Male</option>
                    <option>Female</option>
                    <option>Other</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Chronic Conditions</label>
                <div className="grid grid-cols-2 gap-2">
                  {['Hypertension', 'Diabetes', 'COPD', 'Heart Failure', 'Renal Disease', 'Obesity'].map(c => (
                    <label key={c} className="flex items-center space-x-2 cursor-pointer p-2 hover:bg-gray-50 rounded">
                      <input
                        type="checkbox"
                        checked={patient.chronic_conditions.includes(c)}
                        onChange={() => handleConditionChange(c)}
                        className="rounded text-blue-600 focus:ring-blue-500 h-4 w-4"
                      />
                      <span className="text-sm text-gray-700">{c}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Recent Admissions (Last 12m)</label>
                <input
                  type="number"
                  value={patient.recent_admissions}
                  onChange={e => setPatient({ ...patient, recent_admissions: parseInt(e.target.value) || 0 })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <button
                onClick={handlePredict}
                disabled={loading}
                className={`w-full py-3 px-6 rounded-xl text-white font-bold text-lg shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5 ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
                  }`}
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Simulating Model...
                  </span>
                ) : 'Assess Risk'}
              </button>
            </div>
          </div>

          {/* Results Panel */}
          <div className="space-y-6">
            {prediction ? (
              <>
                <div className="bg-white rounded-2xl shadow-xl overflow-hidden border-t-4 border-indigo-500">
                  <div className="p-6">
                    <h3 className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-1">Assessment Result</h3>
                    <div className="flex items-baseline gap-4">
                      <span className={`text-5xl font-extrabold ${prediction.risk_level === 'High Risk' ? 'text-red-500' :
                          prediction.risk_level === 'Moderate Risk' ? 'text-amber-500' : 'text-emerald-500'
                        }`}>
                        {prediction.risk_level}
                      </span>
                      <span className="text-gray-400 font-medium">
                        {(prediction.confidence * 100).toFixed(1)}% Confidence
                      </span>
                    </div>

                    <div className="mt-8 grid grid-cols-2 gap-6">
                      <div className="h-48">
                        <Doughnut
                          data={{
                            labels: Object.keys(prediction.probability_distribution),
                            datasets: [{
                              data: Object.values(prediction.probability_distribution),
                              backgroundColor: ['#10b981', '#f59e0b', '#ef4444'],
                              borderWidth: 0
                            }]
                          }}
                          options={{
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: { legend: { position: 'right' } }
                          }}
                        />
                      </div>
                      <div className="flex flex-col justify-center space-y-2 text-sm text-gray-600">
                        <p>Based on {patient.chronic_conditions.length} active conditions</p>
                        <p>Age Factor: {patient.age}</p>
                        <p>History: {patient.recent_admissions} previous admits</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-purple-100">
                  <div className="p-6">
                    <button
                      onClick={handleAnalyze}
                      disabled={analyzing}
                      className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl flex items-center justify-center gap-2 shadow-md transition-all"
                    >
                      {analyzing ? 'Consulting Risk AI...' : '✨ Generate Clinical Report'}
                    </button>

                    {analysis && (
                      <div className="mt-6 bg-purple-50 rounded-xl p-6 border border-purple-100">
                        <div className="flex items-start gap-3">
                          <div className="p-2 bg-purple-100 rounded-lg">
                            <span className="text-xl">🤖</span>
                          </div>
                          <div className="prose prose-purple max-w-none">
                            <h4 className="text-purple-900 font-bold mb-2">Clinical Analysis</h4>
                            <p className="text-purple-800 whitespace-pre-line leading-relaxed">{analysis}</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </>
            ) : (
              <div className="h-full bg-white rounded-2xl shadow-sm border border-dashed border-gray-300 flex flex-col items-center justify-center text-gray-400 p-12 text-center">
                <svg className="w-16 h-16 mb-4 text-gray-200" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p className="text-lg font-medium">Ready to Analyze</p>
                <p className="text-sm mt-2">Enter patient vitals and history to stratify readmission risk.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
