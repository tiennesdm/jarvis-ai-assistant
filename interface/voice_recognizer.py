"""Voice recognition module for Jarvis AI."""
import logging
import os
import sys
from typing import Optional

import config

logger = logging.getLogger(__name__)


class VoiceRecognizer:
    """Voice recognition using SpeechRecognition library."""

    def __init__(self):
        self.recognizer = None
        self.microphone = None
        self._init_recognizer()

    def _init_recognizer(self):
        """Initialize speech recognition."""
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.recognizer.energy_threshold = 300
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8

            try:
                self.microphone = sr.Microphone()
                # Calibrate for ambient noise
                with self.microphone as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
                logger.info("Microphone initialized successfully")
            except Exception as e:
                logger.warning(f"Microphone not available: {e}")
                self.microphone = None
        except ImportError:
            logger.warning("SpeechRecognition library not installed. Voice input disabled.")
            self.recognizer = None

    def is_available(self) -> bool:
        """Check if voice recognition is available."""
        return self.recognizer is not None and self.microphone is not None

    def listen(self, timeout: int = 10, phrase_time_limit: int = 15) -> str:
        """Listen from microphone and return recognized text."""
        if not self.is_available():
            return self._text_input_fallback()

        try:
            import speech_recognition as sr

            print("\n🎤 Sun raha hoon... (boliye)")
            with self.microphone as source:
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

            print("🔊 Processing...")

            # Try recognizing in both Hindi and English
            text = None

            # First try with user's default language
            try:
                text = self.recognizer.recognize_google(audio, language=config.VOICE_LANGUAGE)
            except sr.UnknownValueError:
                # Try English
                try:
                    text = self.recognizer.recognize_google(audio, language=config.VOICE_LANGUAGE_EN)
                except sr.UnknownValueError:
                    pass

            if text:
                print(f"✅ Recognized: {text}")
                return text
            else:
                print("❌ Kuch samajh nahi aaya, kripaya dobara boliye.")
                return self._text_input_fallback()

        except sr.WaitTimeoutError:
            print("⏱️ Timeout - kuch nahi suna. Text se input dein:")
            return self._text_input_fallback()
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            print(f"❌ Internet issue: {e}")
            return self._text_input_fallback()
        except Exception as e:
            logger.error(f"Unexpected error in voice recognition: {e}")
            return self._text_input_fallback()

    def listen_continuous(self, callback):
        """Continuously listen in background."""
        if not self.is_available():
            logger.error("Cannot start continuous listening - mic not available")
            return

        import speech_recognition as sr

        def recognizer_callback(recognizer, audio):
            try:
                text = recognizer.recognize_google(audio, language=config.VOICE_LANGUAGE)
                callback(text)
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                logger.error(f"Recognition error: {e}")

        stop_listening = self.recognizer.listen_in_background(self.microphone, recognizer_callback)
        return stop_listening

    def _text_input_fallback(self) -> str:
        """Fallback to text input when voice is not available."""
        try:
            command = input("✏️ Type command: ")
            return command
        except (EOFError, KeyboardInterrupt):
            return "exit"


class TextInput:
    """Text-based input handler."""

    def get_input(self, prompt: str = "Jarvis> ") -> str:
        """Get text input from user."""
        try:
            return input(prompt)
        except (EOFError, KeyboardInterrupt):
            return "exit"

    def confirm(self, message: str) -> bool:
        """Ask yes/no confirmation."""
        response = input(f"{message} (haan/nahi): ").lower().strip()
        return response in ['haan', 'han', 'yes', 'y', 'h', 'ha']
