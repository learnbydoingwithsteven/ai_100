import { useState } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8005';

interface LesionData {
  asymmetry_score: number;
  border_irregularity: number;
  color_variation: number;
  diameter_mm: number;
  evolution: boolean;
}

interface PredictionResult {
  risk_level: string;
  confidence: number;
  probability_distribution: Record<string, number>;
}

function App() {
  const [lesion, setLesion] = useState<LesionData>({
    asymmetry_score: 2,
    border_irregularity: 3,
    color_variation: 2,
    diameter_mm: 5.5,
    evolution: false
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
      const response = await axios.post(`${API_URL}/api/v1/predict`, lesion);
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
        lesion_data: lesion,
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
            🔬 Skin Lesion Classifier
          </h1>
          <p className="text-xl text-gray-600">Melanoma Detection Assistant (ABCD Rule)</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Form */}
          <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
            <div className="bg-blue-600 p-4">
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                🔍 ABCD Assessment
              </h2>
            </div>
            <div className="p-6 space-y-6">

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Asymmetry (0-10)
                  <span className="text-xs text-gray-400 ml-2">How asymmetric is the shape?</span>
                </label>
                <input
                  type="range"
                  min="0"
                  max="10"
                  step="0.5"
                  value={lesion.asymmetry_score}
                  onChange={e => setLesion({ ...lesion, asymmetry_score: parseFloat(e.target.value) })}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-right text-sm font-bold text-blue-600">{lesion.asymmetry_score}</div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Border Irregularity (0-10)
                  <span className="text-xs text-gray-400 ml-2">Jagged or blurred edges?</span>
                </label>
                <input
                  type="range"
                  min="0"
                  max="10"
                  step="0.5"
                  value={lesion.border_irregularity}
                  onChange={e => setLesion({ ...lesion, border_irregularity: parseFloat(e.target.value) })}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-right text-sm font-bold text-blue-600">{lesion.border_irregularity}</div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Color Variation (1-6)
                  <span className="text-xs text-gray-400 ml-2">Number of distinct colors?</span>
                </label>
                <input
                  type="range"
                  min="1"
                  max="6"
                  step="1"
                  value={lesion.color_variation}
                  onChange={e => setLesion({ ...lesion, color_variation: parseInt(e.target.value) })}
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <div className="text-right text-sm font-bold text-blue-600">{lesion.color_variation} Colors</div>
              </div>

              <div className="grid grid-cols-2 gap-4 items-center">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Diameter (mm)</label>
                  <input
                    type="number"
                    value={lesion.diameter_mm}
                    onChange={e => setLesion({ ...lesion, diameter_mm: parseFloat(e.target.value) || 0 })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                  />
                </div>
                <div>
                  <label className="flex items-center space-x-2 cursor-pointer p-2 hover:bg-gray-50 rounded mt-5">
                    <input
                      type="checkbox"
                      checked={lesion.evolution}
                      onChange={e => setLesion({ ...lesion, evolution: e.target.checked })}
                      className="rounded text-blue-600 focus:ring-blue-500 h-5 w-5"
                    />
                    <span className="text-sm font-medium text-gray-700">Evolution (Changing?)</span>
                  </label>
                </div>
              </div>

              <button
                onClick={handlePredict}
                disabled={loading}
                className={`w-full py-3 px-6 rounded-xl text-white font-bold text-lg shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5 ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
                  }`}
              >
                {loading ? 'Analyzing...' : 'Assess Lesion'}
              </button>
            </div>
          </div>

          {/* Results Panel */}
          <div className="space-y-6">
            {prediction ? (
              <>
                <div className="bg-white rounded-2xl shadow-xl overflow-hidden border-t-4 border-indigo-500">
                  <div className="p-6">
                    <h3 className="text-gray-500 text-sm font-semibold uppercase tracking-wider mb-1">Classification Result</h3>
                    <div className="flex items-baseline gap-4">
                      <span className={`text-5xl font-extrabold ${prediction.risk_level === 'Malignant' ? 'text-red-600' :
                          prediction.risk_level === 'Suspicious' ? 'text-amber-500' : 'text-emerald-500'
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
                            backgroundColor: ['#10b981', '#f59e0b', '#dc2626'],
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
                      {analyzing ? 'Consulting Dermatologist AI...' : '✨ Generate Detailed Report'}
                    </button>

                    {analysis && (
                      <div className="mt-6 bg-purple-50 rounded-xl p-6 border border-purple-100">
                        <div className="flex items-start gap-3">
                          <div className="text-2xl">📋</div>
                          <div className="prose prose-purple max-w-none">
                            <h4 className="text-purple-900 font-bold mb-2">Dermatologist Assistant Note</h4>
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
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                <p className="text-lg font-medium">No Analysis Yet</p>
                <p className="text-sm mt-2">Adjust the ABCD sliders to assess a skin lesion.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
