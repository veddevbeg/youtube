from flask import Flask, render_template, request, send_file, redirect, url_for
from pytube import YouTube
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Define the directory for saving files
DOWNLOADS_DIRECTORY = "./downloads"

# Ensure the directory exists
os.makedirs(DOWNLOADS_DIRECTORY, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        download_option = request.form.get("download_option")

        if video_url:
            if download_option == "video":
                filename = download_video(video_url)
            elif download_option == "audio":
                filename = download_audio(video_url)

            if filename:
                return render_template("index.html", download_link=filename)

    return render_template("index.html")

def download_video(video_url):
    video = YouTube(video_url)
    video_stream = video.streams.get_highest_resolution()

    # Generate a safe and unique filename
    original_filename = secure_filename(video.title)  # Get the original title of the video
    filename = original_filename + ".mp4"
    file_path = os.path.join(DOWNLOADS_DIRECTORY, filename)

    try:
        video_stream.download(output_path=DOWNLOADS_DIRECTORY, filename=filename)
        return filename
    except:
        return None

def download_audio(video_url):
    video = YouTube(video_url)
    audio_stream = video.streams.filter(only_audio=True).first()

    # Generate a safe and unique filename
    original_filename = secure_filename(video.title)  # Get the original title of the video
    filename = original_filename + ".mp3"
    file_path = os.path.join(DOWNLOADS_DIRECTORY, filename)

    try:
        audio_stream.download(output_path=DOWNLOADS_DIRECTORY, filename=filename)
        return filename
    except:
        return None

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(DOWNLOADS_DIRECTORY, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
