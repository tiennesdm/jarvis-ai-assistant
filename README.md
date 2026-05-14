# 🤖 JARVIS AI — Your Voice-Controlled OS Automation Assistant

A powerful AI assistant that controls your entire operating system through **voice or text commands** in **Hindi** and **English**. Ask it to open Excel and apply formulas, send WhatsApp messages, edit photos, search the web — it understands, asks clarifying questions when needed, and executes safely.

---

## ✨ Features

### 🎙️ Voice & Text Input
- Speak in **Hindi** or **English** — Jarvis understands both
- Automatic speech recognition with text fallback
- Smart language detection

### 📊 Excel Automation
```
User: "Excel kholo aur SUM formula lagao"
Jarvis: ✅ Excel opened, SUM formula applied!
```
- Open Excel, create workbooks
- Apply formulas (SUM, AVERAGE, COUNT, MAX, MIN)
- Enter data in specific cells
- Format cells, save files

### 💬 WhatsApp Messaging
```
User: "WhatsApp pe Rahul ko message bhejo"
Jarvis: ❓ Kis ko message bhejna hai?
User: "Rahul"
Jarvis: ❓ Kya message bhejna hai?
User: "Kal milte hain"
Jarvis: ✅ Message bhej diya!
```
- Send messages via WhatsApp Web
- Search contacts, send media files
- Direct messaging via wa.me links

### 🖼️ Photo Editing
```
User: "Gallery mein photo crop karo"
Jarvis: ✅ Photo edit mode activated!
```
- Open gallery/photos app
- Crop, rotate, apply filters
- Adjust brightness, save edits

### 🌐 Browser Control
- Navigate to any website
- Google search
- Click, scroll, take screenshots

### 🛡️ Safety First
- **Confirmation for destructive actions** — delete, format, uninstall
- **Dangerous command detection** — blocks rm -rf, format, etc.
- **Smart clarification** — asks when intent is unclear
- **No unsafe operations without approval**

---

## 🏗️ Architecture

```
User Command (Voice/Text)
    ↓
┌─────────────────────────────────────┐
│  Voice Recognizer / Text Input      │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│  Intent Parser (LLM Engine)         │  ← Groq/OpenAI/Local fallback
│  - Extracts: app, action, params    │
│  - Confidence scoring               │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│  Clarification Engine               │
│  - Confidence < 0.7? Ask user ✋    │
│  - Missing params? Ask user ❓      │
│  - Ambiguous action? Clarify 🤔     │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│  Task Planner                       │
│  - Multi-step workflow breakdown    │
│  - Step lifecycle management        │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│  Safety Guard 🛡️                     │
│  - Destructive? Ask confirmation ⚠️ │
│  - Dangerous? Block 🚫              │
└──────────────────┬──────────────────┘
                   ↓
┌─────────────────────────────────────┐
│  Execution Engine                   │
│  ├─ App Manager (open/focus apps)  │
│  ├─ Desktop Control (mouse, keys)  │
│  ├─ Vision Analyzer (OCR, screen)  │
│  ├─ Excel Actions                   │
│  ├─ WhatsApp Actions                │
│  ├─ Photo Actions                   │
│  └─ Browser Actions                 │
└─────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Windows 10/11 (primary), macOS/Linux (partial)
- Microphone (for voice mode)

### Installation

```bash
# Clone/download the project
cd jarvis_ai

# Install dependencies
pip install -r requirements.txt

# Set your LLM API key (optional - works without it too!)
export GROQ_API_KEY="your-groq-api-key-here"   # Optional, for better AI
export OPENAI_API_KEY="your-openai-key-here"   # Alternative

# Run Jarvis
python main.py                    # Text mode (default)
python main.py --voice            # Voice mode
python main.py -c "Excel kholo"   # Single command
```

### Usage Examples

| Command (Hindi) | What It Does |
|------------------|-------------|
| `Excel kholo aur SUM formula lagao` | Opens Excel, applies SUM |
| `WhatsApp pe Rahul ko message bhejo` | Opens WhatsApp, asks for message |
| `Gallery mein photo crop karo` | Opens Photos, starts crop |
| `Chrome mein Google search karo` | Opens Chrome, searches Google |
| `Calculator kholo` | Opens Calculator |
| `Notepad mein likho` | Opens Notepad |

---

## 📁 Project Structure

```
jarvis_ai/
├── main.py              # Entry point
├── config.py            # Settings & API keys
├── requirements.txt     # Dependencies
├── core/                # Brain - orchestrator, planner, session
├── interface/           # Voice & text input
├── intelligence/        # LLM, intent parsing, clarification
├── automation/          # Desktop control, app manager, vision
├── actions/             # App-specific actions (Excel, WhatsApp, etc.)
├── utils/               # Logging, safety, helpers
└── tests/               # Test suite
```

---

## 🔑 Supported Applications

| App | Actions |
|-----|---------|
| **Excel** | Open, create workbook, apply formulas, enter data, save |
| **WhatsApp** | Open, search contacts, send message/media |
| **Gallery/Photos** | View, crop, rotate, filter, adjust brightness |
| **Chrome/Edge** | Navigate, search, click, scroll |
| **Calculator** | Open |
| **Notepad** | Open, type |
| **VS Code** | Open |
| **Spotify** | Open |

---

## ⚙️ Configuration

Edit `config.py` or set environment variables:

```python
# LLM Provider
GROQ_API_KEY = "your-key"      # Fast & cheap (recommended)
OPENAI_API_KEY = "your-key"    # Alternative

# Voice
VOICE_LANGUAGE = "hi-IN"       # Hindi
VOICE_LANGUAGE_EN = "en-US"    # English

# Safety
REQUIRE_CONFIRMATION = True    # Always confirm destructive actions
CONFIDENCE_THRESHOLD = 0.7     # When to ask clarifying questions
```

---

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Test specific module
python tests/test_desktop.py
python tests/test_app_manager.py
```

---

## 🤝 How It Works — Clarification Flow

```
User: "message bhejo"          ← Unclear command
Jarvis: "Kis app se? WhatsApp 
         ya kuch aur?"         ← Clarifying question ❓
User: "WhatsApp"               ← Clarification
Jarvis: "Kis ko message bhejna
         hai?"                 ← Another question ❓
User: "Rahul"                  ← More info
Jarvis: "Kya message bhejna
         hai?"                 ← More clarification ❓
User: "Kal milte hain"         ← Final detail
Jarvis: ✅ Message bhej diya!  ← Executed!
```

---

## 🛡️ Safety Features

1. **Destructive Action Confirmation** — Delete, format, uninstall ke liye confirmation mangta hai
2. **Dangerous Command Blocking** — `rm -rf`, `format c:`, etc. block ho jate hain
3. **System App Protection** — Registry, system settings ke changes confirm kiye jate hain
4. **Confidence Threshold** — Jab samajh nahi aata, tab puchta hai

---

## 🔮 Future Enhancements

- [ ] Multi-language support (Tamil, Telugu, Marathi)
- [ ] AI-powered screen understanding (GPT-4V)
- [ ] Plugin system for custom actions
- [ ] Desktop GUI (Tkinter/PyQt)
- [ ] Task scheduling & reminders
- [ ] Smart home integration

---

## 📝 License

MIT License — Free to use, modify, and distribute.

---

<p align="center">
  <b>Made with ❤️ for making computers understand Hindi</b><br>
  <i>Bolo, likho, kuch bhi karo — Jarvis samajhta hai!</i>
</p>
