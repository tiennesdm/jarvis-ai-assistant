"""Clarification engine - asks user when intent is unclear."""
from typing import Dict, Optional
import config


class ClarificationEngine:
    """Decides when and what to ask user for clarification."""
    
    # High-ambiguity actions that always need more info
    AMBIGUOUS_ACTIONS = ["install", "uninstall", "delete", "format", "send_message", "edit"]
    
    # Apps that need confirmation
    SENSITIVE_APPS = ["settings", "system", "registry", "terminal"]
    
    def should_ask_clarification(self, intent: Dict) -> bool:
        """Determine if clarification is needed."""
        # Always clarify if confidence is low
        if intent.get("confidence", 0) < config.CONFIDENCE_THRESHOLD:
            return True
        
        # Always clarify for ambiguous actions
        if intent.get("action") in self.AMBIGUOUS_ACTIONS:
            # Unless we have all required parameters
            params = intent.get("parameters", {})
            if intent["action"] == "send_message" and not params.get("contact"):
                return True
            if intent["action"] == "install" and not params.get("app_name"):
                return True
        
        # Clarify if app is sensitive
        if intent.get("app_needed") in self.SENSITIVE_APPS:
            return True
        
        # Clarify if intent explicitly says so
        if intent.get("needs_clarification", False):
            return True
        
        return False
    
    def generate_clarifying_question(self, intent: Dict) -> str:
        """Generate a relevant clarifying question in Hindi/English."""
        # Use LLM-provided question if available
        if intent.get("clarifying_question"):
            return intent["clarifying_question"]
        
        app = intent.get("app_needed")
        action = intent.get("action")
        params = intent.get("parameters", {})
        
        # Context-aware questions
        if action in ["send_message", "message"]:
            if not params.get("contact"):
                return "Kis ko message bhejna hai? Contact name batayein."
            if not params.get("message"):
                return f"{params['contact']} ko kya message bhejna hai?"
        
        if action == "install":
            return "Kaunsa app install karna hai? App name batayein."
        
        if action == "apply_formula":
            if not params.get("formula_type"):
                return "Kaunsa formula lagana hai? (SUM, AVERAGE, COUNT, etc.)"
            if not params.get("cell"):
                return "Kis cell mein formula lagana hai? (jaise A1, B2)"
            if not params.get("range"):
                return "Kis range ka hisab karna hai? (jaise A1:A10)"
        
        if app == "gallery" and action in ["crop", "edit"]:
            return "Kaunsi photo edit karni hai? Photo select karein."
        
        if app and not action:
            return f"{app} mein aap kya karna chahte hain? Thoda detail mein batayein."
        
        # Default question
        return "Main samajh nahi paya. Kripaya thoda aur detail mein batayein aap kya karwana chahte hain?"
    
    def refine_intent(self, original: Dict, clarification: str) -> Dict:
        """Refine intent based on user's clarification response."""
        refined = original.copy()
        
        # Try to extract additional info from clarification
        clarification_lower = clarification.lower()
        
        # Extract contact name
        if refined.get("action") == "send_message":
            # Simple extraction - in real app, use LLM
            refined["parameters"] = refined.get("parameters", {}).copy()
            if not refined["parameters"].get("contact"):
                refined["parameters"]["contact"] = clarification.strip()
            elif not refined["parameters"].get("message"):
                refined["parameters"]["message"] = clarification.strip()
        
        # Extract formula details
        if refined.get("action") == "apply_formula":
            refined["parameters"] = refined.get("parameters", {}).copy()
            if "sum" in clarification_lower:
                refined["parameters"]["formula_type"] = "SUM"
            elif "average" in clarification_lower or "avg" in clarification_lower:
                refined["parameters"]["formula_type"] = "AVERAGE"
            elif "count" in clarification_lower:
                refined["parameters"]["formula_type"] = "COUNT"
        
        # Increase confidence after clarification
        refined["confidence"] = min(refined.get("confidence", 0.5) + 0.2, 1.0)
        refined["needs_clarification"] = refined["confidence"] < config.CONFIDENCE_THRESHOLD
        
        return refined
