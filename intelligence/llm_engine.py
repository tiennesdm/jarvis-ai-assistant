"""LLM engine for Jarvis AI - supports Groq, OpenAI, Ollama."""
import os
import json
import re
from typing import Dict, Optional

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    import openai
except ImportError:
    openai = None

import config


class LLMEngine:
    """LLM engine for intent parsing and reasoning."""
    
    SYSTEM_PROMPT = """You are Jarvis, an AI OS Automation Assistant. Your job is to analyze user commands and extract structured intent.

Parse the command and return ONLY a JSON object with this structure:
{
    "app_needed": "name of application (excel, whatsapp, gallery, chrome, etc. or null)",
    "action": "specific action to perform (open, edit, send, formula, etc.)",
    "parameters": {"key": "value"},
    "confidence": 0.0-1.0,
    "needs_clarification": true/false,
    "clarifying_question": "question to ask user if needed, or null",
    "workflow_steps": ["step1", "step2"],
    "is_multi_step": true/false
}

Supported apps: excel, whatsapp, gallery/chrome, vscode, calculator, notepad, browser, spotify

Examples:
- "Excel sheet kholo aur SUM formula lagao" -> app: excel, action: apply_formula
- "WhatsApp pe Rahul ko message bhejo" -> app: whatsapp, action: send_message, needs_clarification: true
- "Gallery mein photo crop karo" -> app: gallery, action: crop_photo
- "Ye app install karo" -> app: null, action: install_app, needs_clarification: true

Respond ONLY with valid JSON."""

    def __init__(self):
        self.client = None
        self.provider = None
        self._init_client()
    
    def _init_client(self):
        """Initialize LLM client with priority: Groq > OpenAI > Ollama."""
        if Groq and config.GROQ_API_KEY and config.GROQ_API_KEY != "your-groq-api-key":
            self.client = Groq(api_key=config.GROQ_API_KEY)
            self.provider = "groq"
            self.model = config.GROQ_MODEL
        elif openai and config.OPENAI_API_KEY:
            self.client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
            self.provider = "openai"
            self.model = config.OPENAI_MODEL
        else:
            self.provider = "local"
            self.model = "local"
    
    def get_response(self, prompt: str, system_context: str = None) -> str:
        """Get response from LLM."""
        system = system_context or self.SYSTEM_PROMPT
        
        try:
            if self.provider == "groq" and self.client:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
                return response.choices[0].message.content
            elif self.provider == "openai" and self.client:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=2000
                )
                return response.choices[0].message.content
            else:
                return self._local_fallback_response(prompt)
        except Exception as e:
            return self._local_fallback_response(prompt)
    
    def _local_fallback_response(self, command: str) -> str:
        """Fallback rule-based parsing when no LLM is available."""
        command_lower = command.lower()
        result = {
            "app_needed": None,
            "action": None,
            "parameters": {},
            "confidence": 0.5,
            "needs_clarification": True,
            "clarifying_question": "Main samajh nahi paya. Kripaya detail mein bataiye aap kya karwana chahte hain?",
            "workflow_steps": [],
            "is_multi_step": False
        }
        
        # App detection
        app_keywords = {
            "excel": ["excel", "spreadsheet", "sheet", "workbook", "formula", "cell"],
            "whatsapp": ["whatsapp", "message", "bhejo", "send", "chat", "msg"],
            "gallery": ["gallery", "photo", "image", "picture", "crop", "edit photo"],
            "chrome": ["chrome", "browser", "website", "google", "search"],
            "vscode": ["vscode", "code editor", "programming"],
            "calculator": ["calculator", "calculate", "calc", "hisab", "jod"],
            "notepad": ["notepad", "notes", "text file", "likho"],
            "spotify": ["spotify", "music", "gaana", "song"],
        }
        
        for app, keywords in app_keywords.items():
            if any(kw in command_lower for kw in keywords):
                result["app_needed"] = app
                result["confidence"] = 0.7
                break
        
        # Action detection
        action_keywords = {
            "open": ["kholo", "open", "start", "launch"],
            "send_message": ["bhejo", "send", "message", "msg", "text"],
            "apply_formula": ["formula", "calculate", "sum", "average", "count"],
            "crop_photo": ["crop", "edit photo", "photo edit"],
            "search": ["search", "khojo", "find", "dhundo"],
            "install": ["install", "download", "setup", "layo"],
            "type": ["type", "likho", "enter", "dalo"],
            "click": ["click", "daba", "select"],
        }
        
        for action, keywords in action_keywords.items():
            if any(kw in command_lower for kw in keywords):
                result["action"] = action
                result["confidence"] = min(result["confidence"] + 0.1, 1.0)
                break
        
        # Detect parameters
        if "sum" in command_lower:
            result["parameters"]["formula_type"] = "SUM"
        if "average" in command_lower or "avg" in command_lower:
            result["parameters"]["formula_type"] = "AVERAGE"
        
        # Detect contact names
        contact_match = re.search(r'(?:ko|to|pe)\s+([A-Z][a-z]+)', command)
        if contact_match:
            result["parameters"]["contact"] = contact_match.group(1)
        
        # Detect cell references
        cell_match = re.search(r'([A-Z]\d+)', command, re.IGNORECASE)
        if cell_match:
            result["parameters"]["cell"] = cell_match.group(1).upper()
        
        if result["app_needed"] and result["action"]:
            result["needs_clarification"] = False
            result["clarifying_question"] = None
            result["confidence"] = min(result["confidence"] + 0.2, 1.0)
        
        result["workflow_steps"] = [f"{result['action']} in {result['app_needed']}"] if result['app_needed'] else []
        result["is_multi_step"] = len(result["workflow_steps"]) > 1
        
        return json.dumps(result, ensure_ascii=False)
    
    def analyze_task(self, command: str) -> Dict:
        """Analyze user command and return structured intent."""
        response = self.get_response(command)
        
        # Extract JSON from response
        try:
            # Try to find JSON in response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                intent = json.loads(json_match.group())
            else:
                intent = json.loads(response)
            
            # Ensure all required fields
            intent.setdefault("app_needed", None)
            intent.setdefault("action", None)
            intent.setdefault("parameters", {})
            intent.setdefault("confidence", 0.5)
            intent.setdefault("needs_clarification", True)
            intent.setdefault("clarifying_question", None)
            intent.setdefault("workflow_steps", [])
            intent.setdefault("is_multi_step", False)
            
            return intent
            
        except (json.JSONDecodeError, Exception) as e:
            # Return safe default with clarification
            return {
                "app_needed": None,
                "action": None,
                "parameters": {},
                "confidence": 0.3,
                "needs_clarification": True,
                "clarifying_question": f"Main thoda confuse hoon. Kya aap thoda aur detail de sakte hain? (Error: {str(e)})",
                "workflow_steps": [],
                "is_multi_step": False
            }
