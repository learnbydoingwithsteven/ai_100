from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

class DiabetesSpecialist:
    def __init__(self):
        # Diabetes Specialist Persona
        self.llm = Ollama(model="qwen2.5:1.5b") 

    def analyze_progression(self, clinical_data: dict) -> str:
        prompt = f"""
        You are an Endocrinologist AI specializing in Diabetes Management.
        Analyze the following patient metrics to assess diabetes progression risk:
        
        Patient Metrics: {clinical_data.get('patient_context', 'Unknown')}
        
        Predicted Risk Level: {clinical_data['prediction']}
        Confidence Score: {clinical_data['confidence']:.2f}
        
        1. Interpret the key indicators (Glucose, BMI, HbA1c).
        2. Provide lifestyle and dietary recommendations tailored to the risk level.
        3. Suggest medical follow-up actions.
        
        Keep it professional, encouraging, and under 150 words.
        Disclaimer: AI Generated. Not a medical diagnosis.
        """
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return "Analysis currently unavailable. Please check Ollama connection."
