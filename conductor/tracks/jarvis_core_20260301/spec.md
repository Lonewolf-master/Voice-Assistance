# Track Specification: Jarvis Core STT/TTS & Wake-Word

## 1. Overview
This track focuses on building the foundational components for a completely offline voice assistant named "Jarvis". The system will use Whisper for Speech-to-Text (STT), Coqui TTS for Text-to-Speech (TTS), and a Vosk-based implementation for wake-word detection.

## 2. Goals
- Implement an offline STT module using OpenAI Whisper.
- Implement an offline TTS module using Coqui TTS.
- Implement an offline wake-word detection module for the word "Jarvis".
- Integrate these components into a functional loop: Wake-Word -> STT -> Logic (Placeholder) -> TTS.
- Ensure modular design for independent testing and future extensibility.
- Provide visual feedback in the console for different system states (Listening, Thinking, Speaking).

## 3. Requirements

### 3.1 Speech-to-Text (STT)
- **Model:** OpenAI Whisper (Local execution).
- **Latency:** Prioritize low latency for a responsive feel.
- **Accuracy:** High accuracy for general and technical language.
- **Input:** Real-time audio stream from the microphone.

### 3.2 Text-to-Speech (TTS)
- **Model:** Coqui TTS (Local execution).
- **Voice:** High-quality, natural-sounding British English.
- **Variety:** Support for multiple local voice models.

### 3.3 Wake-Word Detection
- **Model:** Vosk-based (Local execution).
- **Wake-Word:** "Jarvis".
- **Operation:** Continuous background listening with minimal resource usage.

### 3.4 Integration & UX
- **Feedback:** Clear console indicators for "LISTENING", "THINKING", and "SPEAKING".
- **Interaction:** The system should only proceed to STT after the wake-word is detected.
- **Modularity:** Each component (STT, TTS, Wake-Word) should be a separate Python module.

## 4. Technical Constraints
- No external APIs or internet connectivity required during operation.
- Python 3.10+ environment.
- Dependencies: `openai-whisper`, `TTS`, `vosk`, `pyaudio`.

## 5. Success Criteria
- [ ] Wake-word "Jarvis" reliably triggers the assistant.
- [ ] Speech is transcribed accurately and quickly without an internet connection.
- [ ] Text is synthesized into a natural-sounding voice offline.
- [ ] The system provides real-time status feedback in the console.
- [ ] Each module has >80% unit test coverage.
