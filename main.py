from wake_word import WakeWordModule
from stt import STTModule
from tts import TTSModule
import os
import time

class JarvisAssistant:
    """
    JarvisAssistant coordinates the voice assistant loop: 
    Wake-Word -> STT -> Logic -> TTS.
    """
    
    def __init__(self, ww_model="model", stt_model="base", tts_model="tts_models/en/jenny/vits"):
        """
        Initializes the assistant with its core modules.
        """
        print("Initializing Jarvis...")
        self.wake_word_module = WakeWordModule(model_path=ww_model)
        self.stt_module = STTModule(model_size=stt_model)
        self.tts_module = TTSModule(model_name=tts_model)
        print("Jarvis is ready.")
        
    def capture_audio(self, duration=5):
        """
        Placeholder for capturing a command audio clip after wake-word detection.
        In a full implementation, this would use PyAudio to record.
        """
        # For MVP, we'll return a path (mocked in tests)
        return "command.wav"
        
    def run_once(self):
        """
        Executes one iteration of the assistant loop.
        """
        print("\n[STATUS] LISTENING for wake-word...")
        if self.wake_word_module.listen():
            print("[STATUS] WAKE-WORD DETECTED")
            
            # Step 1: Capture speech
            print("[STATUS] LISTENING for command...")
            audio_path = self.capture_audio()
            
            # Step 2: Transcribe
            print("[STATUS] THINKING (Transcribing)...")
            text = self.stt_module.transcribe(audio_path)
            print(f"[USER] {text}")
            
            # Step 3: Logic (MVP: Echo back)
            response = f"You said: {text}"
            
            # Step 4: Synthesize response
            print("[STATUS] SPEAKING...")
            self.tts_module.speak(response)
            print(f"[JARVIS] {response}")
            
    def start(self):
        """
        Starts the infinite loop for the assistant.
        """
        try:
            while True:
                self.run_once()
        except KeyboardInterrupt:
            print("\nShutting down Jarvis. Goodbye.")

if __name__ == "__main__":
    # Entry point for the application
    assistant = JarvisAssistant()
    assistant.start()
