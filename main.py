from wake_word import WakeWordModule
from stt import STTModule
from tts import TTSModule
from brain import JarvisBrain
import os
import time
import webrtcvad
import collections

class JarvisAssistant:
    """
    JarvisAssistant coordinates the voice assistant loop: 
    Wake-Word -> STT -> AI Logic -> TTS.
    """
    
    def __init__(self, ww_model="model", stt_model="base", tts_model="tts_models/en/jenny/jenny"):
        """
        Initializes the assistant with its core modules.
        """
        print("Initializing Jarvis...")
        self.wake_word_module = WakeWordModule(model_path=ww_model)
        self.stt_module = STTModule(model_size=stt_model)
        self.tts_module = TTSModule(model_name=tts_model)
        self.brain = JarvisBrain()
        self.vad = webrtcvad.Vad(3) # Aggressiveness 0-3
        print("Jarvis is ready.")
        
    def capture_audio(self):
        """
        Captures audio from the microphone until silence is detected (VAD).
        """
        import pyaudio
        import wave
        
        chunk = 480 # 30ms for 16kHz
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 16000
        filename = "command.wav"
        
        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format, channels=channels, rate=fs, 
                        frames_per_buffer=chunk, input=True)
        
        print("[STATUS] LISTENING for command...")
        frames = []
        silent_chunks = 0
        max_silent_chunks = 40 # ~1.2 seconds of silence
        speaking = False
        
        while True:
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
            
            is_speech = self.vad.is_speech(data, fs)
            
            if is_speech:
                speaking = True
                silent_chunks = 0
            elif speaking:
                silent_chunks += 1
                
            if silent_chunks > max_silent_chunks:
                break
                
            # Timeout after 10 seconds total to prevent infinite loop
            if len(frames) > (fs / chunk * 10):
                break
            
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return filename
        
    def run_once(self):
        """
        Executes one iteration of the assistant loop.
        """
        print("\n[STATUS] LISTENING for wake-word...")
        if self.wake_word_module.listen():
            print("[STATUS] WAKE-WORD DETECTED")
            
            # Step 1: Capture speech with VAD
            audio_path = self.capture_audio()
            
            # Step 2: Transcribe with noise reduction (now internal to STT)
            print("[STATUS] THINKING (Transcribing)...")
            text = self.stt_module.transcribe(audio_path)
            print(f"[USER] {text}")
            
            if not text:
                print("[STATUS] NO SPEECH DETECTED")
                return

            # Step 3: AI Brain Logic (Prediction and Response)
            print("[STATUS] THINKING (AI Brain)...")
            response = self.brain.think(text)
            
            # Step 4: Synthesize response and play
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
