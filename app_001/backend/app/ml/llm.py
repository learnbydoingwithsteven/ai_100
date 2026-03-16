from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

class MedicalAssistant:
    def __init__(self):
        # Using a lightweight model by default, assuming user receives "llama3" or "mistral" or similar
        # For now, let's try 'llama3' which is common, or fall back to 'phi' if needed.
        # Given the user request "use ollama", we assume models are present.
        # Using the available qwen2.5:1.5b model
        self.llm = Ollama(model="qwen2.5:1.5b") 

    def analyze_prediction(self, prediction_data: dict) -> str:
        patient_info = prediction_data.get('patient_data', {})
        patient_context = f"Patient: {patient_info.get('age', 'Unknown')}yo {patient_info.get('gender', 'Unknown')}\nSymptoms: {patient_info.get('symptoms', 'None provided')}"
        
        prompt = f"""
        You are a medical AI assistant. 
        Analyze the following prediction results from a medical image diagnosis system:
        
        {patient_context}
        
        Diagnosis: {prediction_data['prediction']}
        Confidence: {prediction_data['confidence']:.2f}
        Probabilities: {prediction_data['probabilities']}
        
        Provide a brief, professional summary of these findings for a doctor, considering the patient context.
        Include a recommendation for next steps.
        Keep it under 150 words.
        Disclaimer: This is AI generated.
        """
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return "Analysis currently unavailable. Please check Ollama connection."
