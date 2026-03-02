import pyaudio

def list_microphones():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')
    
    print("\n--- Available Input Devices ---")
    for i in range(0, num_devices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        if device_info.get('maxInputChannels') > 0:
            print(f"Index {i}: {device_info.get('name')} (Channels: {device_info.get('maxInputChannels')})")
    
    try:
        default_device = p.get_default_input_device_info()
        print(f"\n--- Default Input Device ---")
        print(f"Index {default_device['index']}: {default_device['name']}")
    except Exception as e:
        print(f"\nCould not determine default input device: {e}")
    
    p.terminate()

if __name__ == "__main__":
    list_microphones()
