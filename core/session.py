"""Session state management for Jarvis AI."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
import json
import os


@dataclass
class SessionState:
    """Tracks current session state."""
    session_id: str = field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    current_app: Optional[str] = None
    pending_action: Optional[Dict] = None
    last_screenshot: Optional[str] = None
    conversation_history: List[Dict] = field(default_factory=list)
    context: Dict = field(default_factory=dict)
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
    
    def set_current_app(self, app_name: str):
        """Set currently focused application."""
        self.current_app = app_name
    
    def update_context(self, key: str, value):
        """Update session context."""
        self.context[key] = value
    
    def save(self, filepath: str = None):
        """Save session state to file."""
        if filepath is None:
            filepath = os.path.join(os.path.expanduser("~"), ".jarvis", f"session_{self.session_id}.json")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({
                "session_id": self.session_id,
                "current_app": self.current_app,
                "conversation_history": self.conversation_history,
                "context": self.context
            }, f, indent=2)
