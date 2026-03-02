import pyaudio
import numpy as np

def test_stream():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    print("Listening for audio activity... Speak into the mic. (Ctrl+C to stop)")
    try:
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            # Calculate volume/energy
            audio_data = np.frombuffer(data, dtype=np.int16)
            energy = np.abs(audio_data).mean()
            if energy > 50: # Threshold for showing activity
                print(f"Mic Activity Level: {int(energy)} {'#' * (int(energy)//100)}")
    except KeyboardInterrupt:
        print("
Stopped.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    test_stream()
