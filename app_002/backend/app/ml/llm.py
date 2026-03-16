from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

class MolecularAssistant:
    def __init__(self):
        # Using the available qwen2.5:1.5b model
        self.llm = Ollama(model="qwen2.5:1.5b") 

    def analyze_prediction(self, prediction_data: dict) -> str:
        prompt = f"""
        You are a pharmaceutical AI assistant. 
        Analyze the following drug molecule:
        
        SMILES Structure: {prediction_data['smiles']}
        Predicted Property: {prediction_data['prediction']}
        Confidence: {prediction_data['confidence']:.2f}
        
        1. Identify the molecule or class of compounds from the SMILES.
        2. Explain the significance of the predicted property (e.g. solubility, acidity).
        3. Discuss potential pharmaceutical applications.
        
        Keep it under 150 words.
        Disclaimer: This is AI generated.
        """
        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            return "Analysis currently unavailable. Please check Ollama connection."
