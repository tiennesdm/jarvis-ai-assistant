"""Helper utilities for Jarvis AI."""
import os
import time
import platform
from typing import Optional
import logging

logger = logging.getLogger(__name__)


def get_os() -> str:
    """Get operating system name."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    else:
        return "linux"


def wait(seconds: float = 1.0):
    """Wait for specified seconds."""
    time.sleep(seconds)


def safe_path(path: str) -> str:
    """Convert path to OS-compatible format and expand user."""
    return os.path.expanduser(os.path.normpath(path))


def ensure_dir(path: str):
    """Ensure directory exists."""
    os.makedirs(safe_path(path), exist_ok=True)


def format_time(seconds: float) -> str:
    """Format seconds to readable string."""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    else:
        return f"{seconds/3600:.1f} hours"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length."""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."


def print_banner():
    """Print Jarvis startup banner."""
    banner = """
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║           🤖 JARVIS AI ASSISTANT             ║
    ║                                              ║
    ║     Your Voice-Controlled OS Automation      ║
    ║              Assistant                       ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝

    Commands:
    • "Excel kholo aur SUM formula lagao"
    • "WhatsApp pe Rahul ko message bhejo"
    • "Gallery mein photo edit karo"
    • "type: <command>" for text input
    • "exit" to quit

    """
    print(banner)


def print_response(response: dict):
    """Pretty print assistant response."""
    status = response.get("status", "unknown")
    message = response.get("message", "")

    status_icons = {
        "success": "✅",
        "error": "❌",
        "needs_clarification": "❓",
        "cancelled": "🚫",
        "planned": "📋",
    }

    icon = status_icons.get(status, "ℹ️")
    print(f"\n{icon} {message}\n")
