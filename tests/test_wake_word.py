import pytest
import json
from unittest.mock import MagicMock, patch
from wake_word import WakeWordModule

@pytest.fixture
def wake_word_module():
    with patch("vosk.Model") as mock_model_class, \
         patch("vosk.KaldiRecognizer") as mock_rec_class, \
         patch("pyaudio.PyAudio") as mock_pyaudio_class:
        
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        mock_rec = MagicMock()
        mock_rec_class.return_value = mock_rec
        
        mock_pa = MagicMock()
        mock_pyaudio_class.return_value = mock_pa
        
        module = WakeWordModule(model_path="dummy_model", wake_word="jarvis")
        return module, mock_rec, mock_pa

def test_initialization(wake_word_module):
    module, mock_rec, mock_pa = wake_word_module
    assert module.wake_word == "jarvis"
    assert module.recognizer == mock_rec

def test_listen_and_detect(wake_word_module):
    module, mock_rec, mock_pa = wake_word_module
    
    # Mock stream data
    mock_stream = MagicMock()
    mock_pa.open.return_value = mock_stream
    mock_stream.read.return_value = b"audio_data"
    
    # Simulate recognizer behavior: 
    # Return True when wake word is found
    mock_rec.AcceptWaveform.return_value = True
    mock_rec.Result.return_value = json.dumps({"text": "hello jarvis"})
    
    result = module.listen()
    
    assert result is True
    assert mock_pa.open.called
    assert mock_stream.read.called

def test_listen_no_detection(wake_word_module):
    module, mock_rec, mock_pa = wake_word_module
    
    mock_stream = MagicMock()
    mock_pa.open.return_value = mock_stream
    # Return audio data once, then empty to break the loop
    mock_stream.read.side_effect = [b"audio_data", b""]
    
    # Simulate recognizer behavior: returns True but with different word
    mock_rec.AcceptWaveform.return_value = True
    mock_rec.Result.return_value = json.dumps({"text": "hello world"})
    
    result = module.listen()
    
    assert result is False
    assert mock_pa.open.called
