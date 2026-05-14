"""Main orchestrator - coordinates all components."""
import logging
from typing import Dict, Optional

from core.session import SessionState
from core.task_planner import TaskPlanner, TaskPlan
from intelligence.llm_engine import LLMEngine
from intelligence.clarification import ClarificationEngine
from intelligence.intent_parser import IntentParser
from utils.safety import SafetyGuard

logger = logging.getLogger(__name__)


class JarvisOrchestrator:
    """Main orchestrator that coordinates all Jarvis components."""
    
    def __init__(self):
        self.session = SessionState()
        self.task_planner = TaskPlanner()
        self.intent_parser = IntentParser()
        self.clarification = ClarificationEngine()
        self.safety = SafetyGuard()
        self.llm = LLMEngine()
        self.awaiting_clarification = False
        self.current_plan: Optional[TaskPlan] = None
        self.pending_intent: Optional[Dict] = None
    
    def process_command(self, command: str) -> Dict:
        """Main command processing pipeline."""
        logger.info(f"Processing command: {command}")
        self.session.add_to_history("user", command)
        
        # If awaiting clarification, process as clarification response
        if self.awaiting_clarification:
            return self._handle_clarification_response(command)
        
        # Step 1: Parse intent
        intent = self.intent_parser.parse(command)
        logger.info(f"Parsed intent: {intent}")
        
        # Step 2: Check if clarification needed
        if self.clarification.should_ask_clarification(intent):
            self.awaiting_clarification = True
            self.pending_intent = intent
            question = self.clarification.generate_clarifying_question(intent)
            self.session.add_to_history("assistant", question)
            return {
                "status": "needs_clarification",
                "message": question,
                "current_app": self.session.current_app
            }
        
        # Step 3: Execute the task
        return self._execute_intent(intent, command)
    
    def _handle_clarification_response(self, response: str) -> Dict:
        """Handle user's clarification response."""
        self.awaiting_clarification = False
        
        # Refine intent with clarification
        refined = self.clarification.refine_intent(self.pending_intent, response)
        self.pending_intent = None
        
        # Check again if still needs clarification
        if self.clarification.should_ask_clarification(refined):
            self.awaiting_clarification = True
            self.pending_intent = refined
            question = self.clarification.generate_clarifying_question(refined)
            return {
                "status": "needs_clarification",
                "message": question,
                "current_app": self.session.current_app
            }
        
        # Execute with refined intent
        return self._execute_intent(refined, "clarified_command")
    
    def _execute_intent(self, intent: Dict, original_command: str) -> Dict:
        """Execute the parsed intent."""
        # Create task plan
        plan = self.task_planner.create_plan(intent, original_command)
        self.current_plan = plan
        
        # Safety check
        if self.safety.needs_confirmation(intent):
            if not self.safety.confirm_action(intent):
                return {
                    "status": "cancelled",
                    "message": "Action cancelled by user. Koi aur command?",
                    "current_app": self.session.current_app
                }
        
        # Execute plan
        try:
            result = self._execute_workflow(plan)
            self.session.add_to_history("assistant", result.get("message", "Done!"))
            return {
                "status": "success",
                "message": result.get("message", "Task completed successfully!"),
                "current_app": self.session.current_app,
                "steps_completed": plan.current_step
            }
        except Exception as e:
            logger.error(f"Execution error: {e}", exc_info=True)
            return {
                "status": "error",
                "message": f"Kuch galat ho gaya: {str(e)}. Kripaya dobara try karein.",
                "current_app": self.session.current_app
            }
    
    def _execute_workflow(self, plan: TaskPlan) -> Dict:
        """Execute a multi-step workflow."""
        # This will be fully integrated when all modules are ready
        # For now, return planned steps
        steps_info = "\n".join([f"{i+1}. {step.description}" for i, step in enumerate(plan.steps)])
        return {
            "status": "planned",
            "message": f"Task planned:\n{steps_info}\n\n(Execution requires full module integration - desktop automation modules are being built in parallel)",
        }
    
    def get_status(self) -> Dict:
        """Get current status."""
        return {
            "current_app": self.session.current_app,
            "awaiting_clarification": self.awaiting_clarification,
            "session_id": self.session.session_id,
            "command_history_count": len(self.session.conversation_history)
        }
