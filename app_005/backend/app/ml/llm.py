from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

class DermatologistAssistant:
    def __init__(self):
        self.llm = Ollama(model="qwen2.5:1.5b") 

    def analyze_lesion(self, clinical_data: dict) -> str:
        prompt = f"""
        You are a Dermatologist AI Assistant.
        Analyze the following skin lesion ABCD metrics to assess Melanoma risk:
        
        Clinical Findings: {clinical_data.get('patient_context', 'Unknown')}
        
        Predicted Classification: {clinical_data['prediction']}
        Confidence Score: {clinical_data['confidence']:.2f}
        
        1. Explain the significance of the ABCD findings (Asymmetry, Border, Color, Diameter).
        2. Provide recommendations (e.g., "Immediate biopsy recommended" or "Routine monitoring").
        3. Educate the patient on what to watch for.
        
        Keep it professional, empathetic, and under 150 words.
        Disclaimer: AI Generated. This is not a medical diagnosis. Consult a doctor.
        """
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return "Analysis currently unavailable. Please check Ollama connection."
