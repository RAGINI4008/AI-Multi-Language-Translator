import os
import subprocess
import sys

def check():
    print("--- Environment Check ---")
    print(f"Python Executable: {sys.executable}")
    print(f"CWD: {os.getcwd()}")
    
    # Check imageio-ffmpeg
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"imageio-ffmpeg path: {ffmpeg_path}")
        print(f"Exists on disk: {os.path.exists(ffmpeg_path)}")
    except ImportError:
        print("imageio-ffmpeg is NOT installed")
    
    # Check FFmpeg via subprocess
    print("\n--- Subprocess Check ---")
    try:
        # First try raw command
        res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        print("Raw 'ffmpeg' command: SUCCESS")
    except FileNotFoundError:
        print("Raw 'ffmpeg' command: FAILED (FileNotFoundError)")
        
    # Try with imageio-ffmpeg path in env
    try:
        import imageio_ffmpeg
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        env = os.environ.copy()
        env["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + env.get("PATH", "")
        res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, env=env)
        print("'ffmpeg' with imageio path in ENV: SUCCESS")
    except Exception as e:
        print(f"'ffmpeg' with imageio path in ENV: FAILED ({e})")

    # Check common folders
    print("\n--- Common Folders Check ---")
    paths = [
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe"
    ]
    for p in paths:
        print(f"{p}: {'FOUND' if os.path.exists(p) else 'NOT FOUND'}")

if __name__ == "__main__":
    check()
