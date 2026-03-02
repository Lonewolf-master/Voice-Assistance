import vosk
import pyaudio
import json
import os
import numpy as np

class WakeWordModule:
    """
    WakeWordModule handles offline wake-word detection using Vosk and PyAudio.
    """
    
    def __init__(self, model_path="model", wake_word="jarvis"):
        """
        Initializes the wake-word module.
        """
        self.model = vosk.Model(model_path)
        self.wake_word = wake_word.lower()
        # Phonetic aliases for "Jarvis" to help with different accents
        self.aliases = [self.wake_word, "travis", "service", "java", "charvis", "harvest", "office", "garvis"]
        
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        
    def listen(self):
        """
        Listens to the microphone stream until the wake-word or an alias is detected.
        """
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        stream.start_stream()
        
        print(f"\n[SYSTEM] Listening for '{self.wake_word}' (or similar)...")
        
        try:
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                if len(data) == 0:
                    break
                
                # Energy check to show activity
                audio_data = np.frombuffer(data, dtype=np.int16)
                energy = np.abs(audio_data).mean()
                if energy > 100:
                    print(".", end="", flush=True)

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()
                    if any(alias in text for alias in self.aliases):
                        return True
                else:
                    partial_result = json.loads(self.recognizer.PartialResult())
                    partial_text = partial_result.get("partial", "").lower()
                    if any(alias in partial_text for alias in self.aliases):
                        self.recognizer.Reset()
                        return True
        finally:
            # Clean up stream
            stream.stop_stream()
            stream.close()
            
        return False
