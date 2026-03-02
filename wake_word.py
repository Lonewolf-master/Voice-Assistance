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
        - model_path: Path to the local Vosk model directory
        - wake_word: The word to listen for
        """
        if not os.path.exists(model_path):
            # In a real scenario, we'd ensure the model is downloaded
            # For initialization, we'll allow it if mocked in tests
            pass
            
        self.model = vosk.Model(model_path)
        self.wake_word = wake_word.lower()
        # Initialize recognizer with 16kHz sample rate
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        
    def listen(self):
        """
        Listens to the microphone stream until the wake-word is detected.
        Returns True when detected.
        """
        # Open microphone stream
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        stream.start_stream()
        
        try:
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                if len(data) == 0:
                    break
                
                # Energy check to show activity
                audio_data = np.frombuffer(data, dtype=np.int16)
                energy = np.abs(audio_data).mean()
                if energy > 100: # Adjust threshold as needed
                    print(".", end="", flush=True)

                if self.recognizer.AcceptWaveform(data):
                    result = json.loads(self.recognizer.Result())
                    text = result.get("text", "").lower()
                    if self.wake_word in text:
                        return True
                else:
                    partial_result = json.loads(self.recognizer.PartialResult())
                    partial_text = partial_result.get("partial", "").lower()
                    if self.wake_word in partial_text:
                        # Clear recognizer before returning
                        self.recognizer.Reset()
                        return True
        finally:
            # Clean up stream
            stream.stop_stream()
            stream.close()
            
        return False
