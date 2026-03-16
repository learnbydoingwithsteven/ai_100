from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

class RiskAssessmentAssistant:
    def __init__(self):
        # Using the available, robust model confirmed in previous steps
        self.llm = Ollama(model="qwen2.5:1.5b") 

    def analyze_risk(self, risk_data: dict) -> str:
        prompt = f"""
        You are a Clinical Risk Assessment AI.
        Analyze the following patient data to explain their readmission risk:
        
        Patient Profile: {risk_data.get('patient_context', 'Unknown')}
        Risk Factors (Simulated): {risk_data.get('features', 'N/A')}
        
        Predicted Risk Level: {risk_data['prediction']}
        Confidence Score: {risk_data['confidence']:.2f}
        
        1. Summarize the key risk factors based on the context.
        2. Recommend immediate clinical interventions (e.g., "Schedule follow-up in 48h").
        3. Discuss potential complications if untreated.
        
        Keep it professional, concise, and under 150 words.
        Disclaimer: AI Generated. For clinical support only.
        """
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return "Risk analysis currently unavailable. Please check Ollama connection."
