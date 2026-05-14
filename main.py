#!/usr/bin/env python3
"""
🤖 JARVIS AI - Your Voice-Controlled OS Automation Assistant

Main entry point. Supports voice and text commands in Hindi & English.

Examples:
  $ python main.py
  $ python main.py --text
  $ python main.py --command "Excel kholo aur SUM formula lagao"
  $ python main.py --command "WhatsApp pe Rahul ko message bhejo"
  $ python main.py --voice
"""

import argparse
import logging
import signal
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.logger import setup_logger
from utils.helpers import print_banner, print_response
from utils.safety import SafetyGuard
from interface.voice_recognizer import VoiceRecognizer, TextInput
from core.orchestrator import JarvisOrchestrator

logger = setup_logger()


class JarvisApp:
    """Main Jarvis application."""

    def __init__(self, use_voice: bool = False, use_text: bool = False):
        self.orchestrator = JarvisOrchestrator()
        self.voice = VoiceRecognizer()
        self.text_input = TextInput()
        self.safety = SafetyGuard()
        self.use_voice = use_voice and self.voice.is_available()
        self.use_text = use_text or not self.use_voice
        self.running = True

        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully."""
        print("\n\n👋 Jarvis band ho raha hai... Alvida!")
        self.running = False
        sys.exit(0)

    def run(self, single_command: str = None):
        """Run the main loop."""
        print_banner()

        # Single command mode
        if single_command:
            self._process_command(single_command)
            return

        # Interactive mode
        print("🎤 Jarvis taiyaar hai! Aap command de sakte hain.\n")
        print("Commands:")
        print('  • Bol ke: "Excel kholo aur SUM formula lagao"')
        print('  • Type: "WhatsApp pe Rahul ko message bhejo"')
        print('  • Likho: "gallery mein photo edit karo"')
        print('  • "exit" likho ya bolo - band karne ke liye')
        print()

        while self.running:
            try:
                # Get command (voice or text)
                command = self._get_input()

                if not command or command.strip() == "":
                    continue

                # Exit command
                if command.lower().strip() in ["exit", "quit", "band karo", "alvida", "bye"]:
                    print("\n👋 Alvida! Phir milenge.\n")
                    break

                # Status command
                if command.lower().strip() in ["status", "state"]:
                    self._show_status()
                    continue

                # Process command
                self._process_command(command)

            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Main loop error: {e}", exc_info=True)
                print(f"❌ Kuch galat ho gaya: {e}\n")

    def _get_input(self) -> str:
        """Get input from voice or text."""
        if self.use_voice and self.voice.is_available():
            return self.voice.listen()
        else:
            return self.text_input.get_input("🎤 Jarvis> ")

    def _process_command(self, command: str):
        """Process a single command through the orchestrator."""
        # Safety check
        if not self.safety.is_safe_command(command):
            print("\n🚫 Ye command khatarnak lag rahi hai. Main isse execute nahi karunga.\n")
            return

        print(f"\n📥 Command mila: \"{command}\"\n")

        # Process through orchestrator
        result = self.orchestrator.process_command(command)

        # Print response
        print_response(result)

        # If clarification needed, get response and re-process
        while result.get("status") == "needs_clarification":
            clarifying_question = result.get("message", "")

            if self.use_voice and self.voice.is_available():
                print(f"❓ {clarifying_question}")
                clarification = self.voice.listen()
            else:
                clarification = input(f"❓ {clarifying_question}\n💬 Aap: ")

            result = self.orchestrator.process_command(clarification)
            print_response(result)

    def _show_status(self):
        """Show current system status."""
        status = self.orchestrator.get_status()
        print(f"\n📊 Jarvis Status:")
        print(f"   Current App: {status.get('current_app', 'None')}")
        print(f"   Clarification pending: {status.get('awaiting_clarification', False)}")
        print(f"   Session ID: {status.get('session_id', 'N/A')}")
        print(f"   Commands processed: {status.get('command_history_count', 0)}")
        print(f"   Voice available: {self.voice.is_available()}")
        print()


def main():
    """Parse arguments and start Jarvis."""
    parser = argparse.ArgumentParser(
        description="🤖 Jarvis AI - Voice-Controlled OS Automation Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive mode (text)
  python main.py --voice            # Interactive mode (voice)
  python main.py --text             # Force text mode
  python main.py -c "Excel kholo"   # Single command mode
  python main.py -c "WhatsApp pe message bhejo" --voice

Supported Commands:
  📊 Excel    - open, formulas, data entry, formatting
  💬 WhatsApp - send messages, search contacts
  🖼️  Gallery  - photo editing, filters, cropping
  🌐 Browser  - search, navigate, screenshots
  📝 Files    - create, move, copy, delete (with confirmation)
  🖥️  Apps     - open, close, install (guided)
        """
    )
    parser.add_argument(
        "-v", "--voice",
        action="store_true",
        help="Enable voice input mode"
    )
    parser.add_argument(
        "-t", "--text",
        action="store_true",
        help="Force text input mode (default)"
    )
    parser.add_argument(
        "-c", "--command",
        type=str,
        default=None,
        help="Execute single command and exit"
    )

    args = parser.parse_args()

    # Determine input mode
    use_voice = args.voice
    use_text = args.text or (not args.voice)

    # Start Jarvis
    app = JarvisApp(use_voice=use_voice, use_text=use_text)
    app.run(single_command=args.command)


if __name__ == "__main__":
    main()
