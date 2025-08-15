# AI Voice Assistant 🎙🤖

A **voice-activated AI chatbot** built in Python that can:
- Answer questions using **Ollama (LLaMA2)**
- Perform **real-time web searches** with DuckDuckGo
- Fetch the latest **news headlines** from NewsAPI
- Open popular websites on command
- Play songs (with optional `music_library` module)
- Speak naturally using **gTTS** and **pygame**

This assistant listens for the wake word `"hello"` and stays active until you say `"deactivate"`.

---

## ✨ Features

- 🎤 **Voice Recognition** with Google Speech Recognition
- 🗣 **Text-to-Speech** using gTTS + pygame
- 🧠 AI-powered responses from **Ollama LLaMA2**
- 🔎 **Live Search** via DuckDuckGo
- 📰 News updates from **NewsAPI**
- 🌐 Open Google, YouTube, Facebook, Twitter, Instagram
- 🎵 Play music via a custom `music_library` module
- 📴 Wake & sleep mode with `"hello"` and `"deactivate"`

---

## 🎙️ Commands

- "Open Google"

- "What's the news?"

- "Play Shape of You"

- "Who is Albert Einstein?"

- Say "deactivate" to put the assistant back to sleep

---

## ⚠️ Notes

- Requires an active internet connection for voice recognition, AI, and news.

- NewsAPI key is required for the news feature.

- Ollama must be running locally for AI responses.

- Works on Windows, macOS, and Linux.

---

## 🛠 Requirements

### Install Python Dependencies
```bash
pip install speechrecognition pyttsx3 requests pygame gTTS duckduckgo-search python-dotenv
