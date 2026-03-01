import pytest
import os
from unittest.mock import MagicMock, patch
from stt import STTModule

@pytest.fixture
def stt_module():
    with patch("whisper.load_model") as mock_load:
        mock_model = MagicMock()
        mock_load.return_value = mock_model
        module = STTModule(model_size="base")
        return module, mock_model

def test_stt_initialization(stt_module):
    module, mock_model = stt_module
    assert module.model_size == "base"
    assert module.model == mock_model

def test_transcribe(stt_module):
    module, mock_model = stt_module
    mock_model.transcribe.return_value = {"text": "Hello, world!"}
    
    # Mocking a file path and its existence
    audio_path = "dummy_audio.wav"
    with patch("os.path.exists", return_value=True):
        result = module.transcribe(audio_path)
    
    assert result == "Hello, world!"
    mock_model.transcribe.assert_called_once_with(audio_path)

def test_transcribe_error(stt_module):
    module, mock_model = stt_module
    mock_model.transcribe.side_effect = Exception("Transcription error")
    
    audio_path = "dummy_audio.wav"
    with patch("os.path.exists", return_value=True):
        with pytest.raises(Exception, match="Transcription error"):
            module.transcribe(audio_path)

def test_transcribe_file_not_found(stt_module):
    module, mock_model = stt_module
    
    audio_path = "non_existent.wav"
    with patch("os.path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            module.transcribe(audio_path)
