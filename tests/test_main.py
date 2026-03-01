import pytest
from unittest.mock import MagicMock, patch
from main import JarvisAssistant

@pytest.fixture
def assistant():
    with patch("main.WakeWordModule") as mock_ww_class, \
         patch("main.STTModule") as mock_stt_class, \
         patch("main.TTSModule") as mock_tts_class:
        
        mock_ww = MagicMock()
        mock_ww_class.return_value = mock_ww
        
        mock_stt = MagicMock()
        mock_stt_class.return_value = mock_stt
        
        mock_tts = MagicMock()
        mock_tts_class.return_value = mock_tts
        
        assistant = JarvisAssistant()
        return assistant, mock_ww, mock_stt, mock_tts

def test_assistant_initialization(assistant):
    asst, mock_ww, mock_stt, mock_tts = assistant
    assert asst.wake_word_module == mock_ww
    assert asst.stt_module == mock_stt
    assert asst.tts_module == mock_tts

def test_run_once_success(assistant):
    asst, mock_ww, mock_stt, mock_tts = assistant
    
    # Mock successful loop
    mock_ww.listen.return_value = True
    mock_stt.transcribe.return_value = "hello jarvis"
    
    # Run loop once (we'll need a way to break the infinite loop in main.py for testing)
    with patch("main.JarvisAssistant.capture_audio", return_value="dummy.wav"):
        asst.run_once()
    
    mock_ww.listen.assert_called_once()
    mock_stt.transcribe.assert_called_once()
    mock_tts.speak.assert_called_once()

def test_run_once_no_wake_word(assistant):
    asst, mock_ww, mock_stt, mock_tts = assistant
    
    mock_ww.listen.return_value = False
    
    asst.run_once()
    
    mock_ww.listen.assert_called_once()
    mock_stt.transcribe.assert_not_called()
    mock_tts.speak.assert_not_called()

def test_start_graceful_shutdown(assistant):
    asst, mock_ww, mock_stt, mock_tts = assistant
    
    # Mock run_once to raise KeyboardInterrupt
    with patch("main.JarvisAssistant.run_once") as mock_run_once:
        mock_run_once.side_effect = KeyboardInterrupt()
        asst.start()
        mock_run_once.assert_called_once()
