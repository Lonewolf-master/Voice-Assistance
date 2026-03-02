import pytest
import os
from unittest.mock import MagicMock, patch
from tts import TTSModule

@pytest.fixture
def tts_module():
    # Use a valid Coqui TTS model name format
    model_name = "tts_models/en/jenny/jenny"
    with patch("tts.TTS") as mock_tts_class:
        mock_tts_instance = MagicMock()
        mock_tts_class.return_value = mock_tts_instance
        module = TTSModule(model_name=model_name)
        return module, mock_tts_instance

def test_tts_initialization(tts_module):
    module, mock_tts = tts_module
    assert module.model_name == "tts_models/en/jenny/jenny"
    assert module.tts == mock_tts

def test_speak(tts_module):
    module, mock_tts = tts_module
    text = "Hello, I am Jarvis."
    output_path = "output.wav"
    
    module.speak(text, output_path)
    
    mock_tts.tts_to_file.assert_called_once_with(text=text, file_path=output_path)

def test_speak_error(tts_module):
    module, mock_tts = tts_module
    mock_tts.tts_to_file.side_effect = Exception("Synthesis error")
    
    text = "Hello, I am Jarvis."
    output_path = "output.wav"
    
    with pytest.raises(Exception, match="Synthesis error"):
        module.speak(text, output_path)
