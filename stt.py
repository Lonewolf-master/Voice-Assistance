import whisper
import os

class STTModule:
    """
    STTModule handles speech-to-text transcription using a local OpenAI Whisper model.
    """
    
    def __init__(self, model_size="base"):
        """
        Initializes the STT module with the specified Whisper model size.
        - model_size: 'tiny', 'base', 'small', 'medium', 'large'
        """
        self.model_size = model_size
        # Load the Whisper model locally (this may download it on the first run)
        self.model = whisper.load_model(self.model_size)
        
    def transcribe(self, audio_path):
        """
        Transcribes an audio file into text using the loaded Whisper model.
        - audio_path: Path to the .wav or .mp3 file
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        try:
            # Transcribe the audio file and return the text
            result = self.model.transcribe(audio_path)
            return result.get("text", "").strip()
        except Exception as e:
            # Handle transcription errors (e.g., audio file processing error)
            raise Exception(f"Transcription error: {str(e)}")
