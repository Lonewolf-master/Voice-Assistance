# Implementation Plan: Jarvis Core STT/TTS & Wake-Word

## Phase 1: Environment Setup & STT Module [checkpoint: ac3822a]

- [x] **Task: Environment Initialization** ac3822a
  - [ ] Configure Python virtual environment.
  - [ ] Create `requirements.txt` with `openai-whisper`, `TTS`, `vosk`, `pyaudio`, `pytest`, `pytest-cov`.
  - [ ] Verify local installation and access to GPU (if applicable).
- [x] **Task: Implement Offline STT Module** ac3822a
  - [ ] Write unit tests for STT transcription functionality (mocking audio input).
  - [ ] Implement `stt.py` using OpenAI Whisper (local).
  - [ ] Run tests and verify >80% coverage.
- [x] **Task: Conductor - User Manual Verification 'Phase 1: Environment Setup & STT Module' (Protocol in workflow.md)** ac3822a

## Phase 2: TTS Module Implementation [checkpoint: e890361]

- [x] **Task: Implement Offline TTS Module** ac3822a
  - [ ] Write unit tests for TTS synthesis functionality (mocking audio output).
  - [ ] Implement `tts.py` using Coqui TTS (local).
  - [ ] Run tests and verify >80% coverage.
- [x] **Task: Conductor - User Manual Verification 'Phase 2: TTS Module Implementation' (Protocol in workflow.md)** e890361

## Phase 3: Wake-Word Detection Module

- [ ] **Task: Implement Wake-Word Detection**
  - [ ] Write unit tests for wake-word detection (mocking audio input).
  - [ ] Implement `wake_word.py` using Vosk.
  - [ ] Run tests and verify >80% coverage.
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: Wake-Word Detection Module' (Protocol in workflow.md)**

## Phase 4: System Integration & Voice Assistant Loop

- [ ] **Task: Integrate Components into Main Loop**
  - [ ] Create `main.py` to coordinate the flow: Wake-Word -> STT -> Logic -> TTS.
  - [ ] Implement visual indicators for system state (LISTENING, THINKING, SPEAKING).
  - [ ] Perform integration tests to verify the complete loop.
- [ ] **Task: Conductor - User Manual Verification 'Phase 4: System Integration & Voice Assistant Loop' (Protocol in workflow.md)**
