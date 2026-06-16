import sys
import os
import assemblyai as aai
from flask import Flask, request, jsonify, send_from_directory

aai.settings.api_key = "1b3a5c6e5fa54724a9b185a4ccb1dc8f"

def transcribe_audio(audio_path):
    config = aai.TranscriptionConfig(
        speech_models=["universal-2", "universal-3-pro"],
        language_code="id",
    )
    transcript = aai.Transcriber(config=config).transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        return None, transcript.error

    return transcript.text, None

def run_cli():
    if len(sys.argv) < 2:
        print("Usage: python app.py <path_file_audio>")
        sys.exit(1)

    audio_path = sys.argv[1]

    if not os.path.exists(audio_path):
        print(f"Error: File not found — {audio_path}")
        sys.exit(1)

    print(f"Proccessing: {audio_path}")
    print("Please wait...\n")

    text, error = transcribe_audio(audio_path)

    if error:
        print(f"Transcribe Failed: {error}")
        sys.exit(1)

    print("=" * 60)
    print("Transcribe Result")
    print("=" * 60)
    print(text)
    print("=" * 60)

#Flask REST API 
app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("templates", "index.html")

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)

@app.route("/transcribe", methods=["POST"])
def transcribe_api():
    if "file" not in request.files:
        return jsonify({"error": "File not found"})

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "File is empty"})

    temp_path = f"temp_{file.filename}"
    file.save(temp_path)

    text, error = transcribe_audio(temp_path)

    os.remove(temp_path)

    if error:
        return jsonify({"error": error})

    return jsonify({"text": text})


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        print("Running web server...")
        app.run(debug=True)