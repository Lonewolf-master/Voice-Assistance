import whisper
import os
import noisereduce as nr
import numpy as np
import wave

class STTModule:
    """
    STTModule handles speech-to-text transcription using a local OpenAI Whisper model.
    It now includes audio enhancement (noise reduction).
    """
    
    def __init__(self, model_size="base"):
        """
        Initializes the STT module with the specified Whisper model size.
        - model_size: 'tiny', 'base', 'small', 'medium', 'large'
        """
        self.model_size = model_size
        # Load the Whisper model locally (this may download it on the first run)
        self.model = whisper.load_model(self.model_size)
        
    def preprocess_audio(self, audio_path):
        """
        Applies noise reduction to the audio file.
        """
        try:
            with wave.open(audio_path, "rb") as wf:
                sample_rate = wf.getframerate()
                data = wf.readframes(wf.getnframes())
                audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
            
            # Apply noise reduction
            reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)
            
            # Save enhanced audio to a temporary file
            enhanced_path = "enhanced_" + audio_path
            with wave.open(enhanced_path, "wb") as wf_out:
                wf_out.setnchannels(1)
                wf_out.setsampwidth(2)
                wf_out.setframerate(sample_rate)
                wf_out.writeframes(reduced_noise.astype(np.int16).tobytes())
                
            return enhanced_path
        except Exception as e:
            print(f"Warning: Noise reduction failed: {e}")
            return audio_path

    def transcribe(self, audio_path):
        """
        Transcribes an audio file into text using the loaded Whisper model.
        - audio_path: Path to the .wav or .mp3 file
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        # Enhance audio before transcription
        enhanced_audio = self.preprocess_audio(audio_path)
        
        try:
            # Transcribe the enhanced audio (forcing English)
            result = self.model.transcribe(enhanced_audio, language="en")
            return result.get("text", "").strip()
        except Exception as e:
            # Handle transcription errors (e.g., audio file processing error)
            raise Exception(f"Transcription error: {str(e)}")
        finally:
            if enhanced_audio != audio_path and os.path.exists(enhanced_audio):
                os.remove(enhanced_audio)
