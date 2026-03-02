from TTS.api import TTS
import os

class TTSModule:
    """
    TTSModule handles text-to-speech synthesis using a local Coqui TTS model.
    """
    
    def __init__(self, model_name="tts_models/en/jenny/jenny", gpu=True):
        """
        Initializes the TTS module with the specified model and optional GPU support.
        - model_name: Name of the TTS model to load
        - gpu: Boolean to enable/disable CUDA support
        """
        self.model_name = model_name
        # Initialize the TTS model (this may download it on the first run)
        # We specify gpu=True to utilize local hardware acceleration if available
        self.tts = TTS(model_name=self.model_name, gpu=gpu)
        
    def speak(self, text, output_path="output.wav"):
        """
        Synthesizes text into speech and plays it.
        - text: The string to be converted to speech
        - output_path: Path where the resulting WAV file will be saved
        """
        try:
            # Generate the speech and save to the specified file path
            self.tts.tts_to_file(text=text, file_path=output_path)
            # Play the generated audio file
            os.system(f"aplay {output_path} > /dev/null 2>&1")
            return output_path
        except Exception as e:
            # Handle synthesis errors (e.g., model execution or file system error)
            raise Exception(f"Synthesis error: {str(e)}")
            
    def play(self, audio_path):
        """
        Placeholder method for playing audio (to be integrated with pydub or similar if needed).
        Currently, speech is just saved to file as requested.
        """
        # Integration with audio playback libraries could happen here
        pass
