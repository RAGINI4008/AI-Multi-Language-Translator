# 🚀 Hugging Face Spaces Deployment Guide

Your AI Multi-Language Translator is now fully optimized and ready to run on Hugging Face Spaces for free!
I have modified the code to securely record audio from the web browser instead of trying to access a local computer microphone.

Follow these step-by-step instructions:

## Step 1: Create a Hugging Face Account
1. Go to [huggingface.co](https://huggingface.co/) and create a free account if you don't have one.

## Step 2: Create a New Space
1. Click on your profile picture in the top right and select **New Space** (or go to [huggingface.co/new-space](https://huggingface.co/new-space)).
2. Fill out the form:
   - **Space name**: `ai-audio-translator` (or any name you like).
   - **License**: Choose `MIT` or `OpenRAIL`.
   - **Select the Space SDK**: Click on **Streamlit**.
   - **Space hardware**: Keep the default `Free` tier (CPU basic · 16GB · 2 vCPU).
   - **Space Visibility**: Choose `Public`.
3. Click the **Create Space** button.

## Step 3: Upload Your Files
You need to upload the files from your `ai_translator` folder directly into the Hugging Face Space.

1. On your new Space's page, look for the **Files and versions** tab at the top and click it.
2. Click the **Add file** button in the top right, then select **Upload files**.
3. Drag and drop the following files from your local computer (`C:\ai_tran\ai_translator`) into the upload area:
   - `app.py`
   - `requirements.txt` *(Make sure this is the updated one I just created!)*
   - `packages.txt` *(This installs FFmpeg on their server)*
   - `speech_to_text.py`
   - `text_to_speech.py`
   - `translator.py`
   - `language_detection.py`
   - `utils.py`
   - `README.md`
4. Type a commit message (e.g., "Initial upload") and click **Commit changes to main**.

## Step 4: Watch it Build!
1. Click the **App** tab at the top of your Space.
2. You will see a "Building" log. Hugging Face is now installing Python, Streamlit, and FFmpeg (from your `packages.txt`).
3. This usually takes 2-3 minutes.
4. Once it says **Running**, your app will appear on the screen!

## Step 5: Test the Cloud App
1. Go to the **Voice Input** tab in your deployed app.
2. Click the microphone icon. **Your web browser will pop up a message asking for permission to use your microphone. You MUST click Allow.**
3. Record a short message.
4. Note: On the very first run, it might take ~1 minute to download the Whisper and Translation AI models to the cloud server. Subsequent translations will be fast!
