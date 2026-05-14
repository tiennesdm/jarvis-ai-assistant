"""Intent parser - converts raw commands to structured intents."""
from typing import Dict
from intelligence.llm_engine import LLMEngine


class IntentParser:
    """Parses user commands into structured intents."""
    
    def __init__(self):
        self.llm = LLMEngine()
    
    def parse(self, command: str) -> Dict:
        """Parse user command into structured intent."""
        # First try LLM-based parsing
        intent = self.llm.analyze_task(command)
        return intent
