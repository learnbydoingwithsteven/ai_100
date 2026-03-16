import { useState } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8004';

interface PatientVitals {
  glucose_fasting: number;
  hba1c: number;
  bmi: number;
  age: number;
  hypertension: boolean;
}

interface PredictionResult {
  risk_level: string;
  confidence: number;
  probability_distribution: Record<string, number>;
}

function App() {
  const [patient, setPatient] = useState<PatientVitals>({
    glucose_fasting: 95,
    hba1c: 5.4,
    bmi: 24.0,
    age: 45,
    hypertension: false
  });

  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [analysis, setAnalysis] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    setAnalysis('');
    setPrediction(null);
    try {
      const response = await axios.post(`${API_URL}/api/v1/predict`, patient);
      setPrediction(response.data);
    } catch (err) {
      console.error(err);
      alert('Prediction failed. Is backend running?');
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
            🩸 Diabetes Progression AI
          </h1>
          <p className="text-xl text-gray-600">Early Onset Prediction & Management</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="bg-blue-600 p-4">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                📋 Clinical Metrics
              </h2>
            </div>
            <div className="p-6 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Fasting Glucose (mg/dL)</label>
                  <input
                    type="number"
                    value={patient.glucose_fasting}
                    onChange={e => setPatient({ ...patient, glucose_fasting: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">HbA1c (%)</label>
                  <input
                    type="number"
                    step="0.1"
                    value={patient.hba1c}
                    onChange={e => setPatient({ ...patient, hba1c: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">BMI</label>
                  <input
                    type="number"
                    step="0.1"
                    value={patient.bmi}
                    onChange={e => setPatient({ ...patient, bmi: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                  <input
                    type="number"
                    value={patient.age}
                    onChange={e => setPatient({ ...patient, age: parseInt(e.target.value) || 0 })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="flex items-center space-x-2 cursor-pointer p-2 hover:bg-gray-50 rounded">
                  <input
                    type="checkbox"
                    checked={patient.hypertension}
                    onChange={e => setPatient({ ...patient, hypertension: e.target.checked })}
                    className="rounded text-blue-600 focus:ring-blue-500 h-4 w-4"
                  />
                  <span className="text-sm font-medium text-gray-700">Hypertension Diagnosis</span>
                </label>
              </div>

              <button
                onClick={handlePredict}
                disabled={loading}
                className={`w-full py-3 px-6 rounded-xl text-white font-bold text-lg shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5 ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
                  }`}
              >
                {loading ? 'Analyzing...' : 'Assess Progression Risk'}
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

                    <div className="mt-8 flex justify-center h-48">
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
                  </div>
                </div>

                <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-purple-100">
                  <div className="p-6">
                    <button
                      onClick={handleAnalyze}
                      disabled={analyzing}
                      className="w-full bg-purple-600 hover:bg-purple-700 text-white font-bold py-3 px-6 rounded-xl flex items-center justify-center gap-2 shadow-md transition-all"
                    >
                      {analyzing ? 'Consulting Specialist...' : '✨ Generate Endocrinologist Report'}
                    </button>

                    {analysis && (
                      <div className="mt-6 bg-purple-50 rounded-xl p-6 border border-purple-100">
                        <div className="flex items-start gap-3">
                          <div className="text-2xl">🩺</div>
                          <div className="prose prose-purple max-w-none">
                            <h4 className="text-purple-900 font-bold mb-2">Specialist Analysis</h4>
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
                </svg>
                <p className="text-lg font-medium">Awaiting Clinical Data</p>
                <p className="text-sm mt-2">Enter glucose and HbA1c to assess diabetes risk.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
