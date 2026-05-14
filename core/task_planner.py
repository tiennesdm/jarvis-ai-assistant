"""Task planning and decomposition for Jarvis AI."""
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class StepStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TaskStep:
    """Individual step in a task workflow."""
    step_id: int
    description: str
    action: str  # 'open_app', 'click', 'type', 'ask_clarification', 'execute_in_app', 'confirm'
    app: Optional[str] = None
    parameters: Dict = field(default_factory=dict)
    status: StepStatus = StepStatus.PENDING
    result: Optional[str] = None
    requires_confirmation: bool = False
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class TaskPlan:
    """Complete task plan with multiple steps."""
    original_command: str
    steps: List[TaskStep] = field(default_factory=list)
    current_step: int = 0
    is_complete: bool = False
    
    def add_step(self, description: str, action: str, app: str = None, 
                 parameters: Dict = None, requires_confirmation: bool = False):
        """Add a step to the plan."""
        step = TaskStep(
            step_id=len(self.steps),
            description=description,
            action=action,
            app=app,
            parameters=parameters or {},
            requires_confirmation=requires_confirmation
        )
        self.steps.append(step)
        return step
    
    def get_current_step(self) -> Optional[TaskStep]:
        """Get current pending step."""
        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        return None
    
    def mark_step_complete(self, result: str = None):
        """Mark current step as completed."""
        if self.current_step < len(self.steps):
            self.steps[self.current_step].status = StepStatus.COMPLETED
            self.steps[self.current_step].result = result
            self.current_step += 1
            if self.current_step >= len(self.steps):
                self.is_complete = True
    
    def mark_step_failed(self, error: str):
        """Mark current step as failed."""
        if self.current_step < len(self.steps):
            self.steps[self.current_step].status = StepStatus.FAILED
            self.steps[self.current_step].result = error


class TaskPlanner:
    """Plans and decomposes user commands into executable steps."""
    
    def create_plan(self, parsed_intent: Dict, original_command: str) -> TaskPlan:
        """Create execution plan from parsed intent."""
        plan = TaskPlan(original_command=original_command)
        
        app = parsed_intent.get("app_needed")
        action = parsed_intent.get("action")
        params = parsed_intent.get("parameters", {})
        
        # Step 1: Open target app if not already open
        if app:
            plan.add_step(
                description=f"Open {app}",
                action="open_app",
                app=app,
                parameters={"app_name": app}
            )
        
        # Step 2: Perform the main action
        if action:
            plan.add_step(
                description=f"Execute {action}",
                action="execute_in_app",
                app=app,
                parameters={"action": action, **params},
                requires_confirmation=action in ["delete", "format", "install", "uninstall"]
            )
        
        # Step 3: Confirm completion
        plan.add_step(
            description="Confirm task completion",
            action="notify_user",
            parameters={"message": f"Task '{original_command}' completed!"}
        )
        
        return plan
