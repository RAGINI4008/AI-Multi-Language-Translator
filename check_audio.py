import sounddevice as sd
import numpy as np

def check_audio():
    print("--- Audio Device Check ---")
    devices = sd.query_devices()
    print(devices)
    
    default_input = sd.default.device[0]
    print(f"\nDefault Input Device ID: {default_input}")
    
    try:
        device_info = sd.query_devices(default_input, 'input')
        print(f"Device Name: {device_info['name']}")
    except Exception as e:
        print(f"Error querying default device: {e}")

    print("\n--- Testing 3-second recording ---")
    fs = 16000
    duration = 3
    try:
        print("Recording... Speak into your mic!")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        print("Done recording.")
        
        rms = np.sqrt(np.mean(recording**2))
        print(f"Signal Level (RMS): {rms:.6f}")
        
        if rms < 0.0001:
            print("Warning: Signal level is very low. Mic might be muted or incorrect device selected.")
        else:
            print("Success: Audio signal detected!")
            
    except Exception as e:
        print(f"Error during recording test: {e}")

if __name__ == "__main__":
    check_audio()
