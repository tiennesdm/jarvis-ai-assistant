"""Configuration settings for Jarvis AI Assistant."""
import os

# LLM Configuration - Use Groq for fast, cheap inference
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key")
GROQ_MODEL = "llama3-70b-8192"

# OpenAI Fallback
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"

# Voice Recognition
VOICE_ENGINE = "speech_recognition"  # Options: speech_recognition, whisper, vosk
VOICE_LANGUAGE = "hi-IN"  # Default: Hindi
VOICE_LANGUAGE_EN = "en-US"

# Safety Settings
REQUIRE_CONFIRMATION = True
CONFIDENCE_THRESHOLD = 0.7

# Screen Settings
SCREENSHOT_DIR = os.path.join(os.path.expanduser("~"), ".jarvis", "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# App Settings
APP_OPEN_TIMEOUT = 10  # seconds
ACTION_DELAY = 0.5  # seconds between actions
