import os
import imageio_ffmpeg
import subprocess
import sys

def debug_ffmpeg():
    print("--- Debugging FFmpeg ---")
    try:
        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        print(f"FFmpeg Path from imageio: {ffmpeg_path}")
        print(f"Exists: {os.path.exists(ffmpeg_path)}")
        
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        print(f"FFmpeg Directory: {ffmpeg_dir}")
        
        # Add to PATH
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        print(f"Updated PATH starts with: {os.environ['PATH'][:100]}...")
        
        # Test calling ffmpeg
        print("\nTesting 'ffmpeg -version'...")
        try:
            res = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
            print("Success! First line of output:")
            print(res.stdout.splitlines()[0])
        except subprocess.CalledProcessError as e:
            print(f"CalledProcessError: {e}")
            print(f"Stderr: {e.stderr}")
        except FileNotFoundError:
            print("FileNotFoundError: 'ffmpeg' still not found in PATH")
        except Exception as e:
            print(f"Unexpected error calling ffmpeg: {type(e).__name__}: {e}")

    except Exception as e:
        print(f"Error during debugging: {type(e).__name__}: {e}")

if __name__ == "__main__":
    debug_ffmpeg()
