import logging
from flask import Flask, render_template, send_from_directory, request
import os
import re
import subprocess

app = Flask(__name__)
media_directory = "/plex_media"

# Configure logging
logging.basicConfig(level=logging.INFO, filename="/var/log/python-web-server/server.log", format="%(asctime)s - %(levelname)s - %(message)s")

def get_directory_contents(directory_path):
    contents = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, media_directory)
            contents.append(relative_path)
    contents.sort()  # Sort the contents alphabetically
    return contents

@app.route("/", methods=["GET", "POST"])
def index():
    logging.info("Connection to index route")
    if request.method == "POST":
        label_data = request.form.get("labelString")
        magnet_data = request.form.get("magnetString")
        process_form(label_data, magnet_data)  # Call your custom function with the form data
    subdirectories = [name for name in os.listdir(media_directory) if os.path.isdir(os.path.join(media_directory, name))]
    return render_template("index.html", subdirectories=subdirectories)

@app.route("/<path:subdirectory>")
def show_directory(subdirectory):
    logging.info(f"Connection to show_directory route - subdirectory: {subdirectory}")
    directory_path = os.path.join(media_directory, subdirectory)
    contents = get_directory_contents(directory_path)
    return render_template("subdirectory.html", subdirectory=subdirectory, contents=contents)

@app.route("/<path:subdirectory>/<path:filename>")
def download(subdirectory, filename):
    logging.info(f"Connection to download route - subdirectory: {subdirectory}, filename: {filename}")
    return send_from_directory(os.path.join(media_directory, subdirectory), filename)

# Custom Jinja2 filter for regex matching
def regex_match(value, pattern):
    regex = re.compile(pattern)
    return regex.match(value)

# Custom Jinja2 filter to remove duplicate root directory from URLs
def remove_duplicate_root(value, root):
    if value.startswith(root):
        return value[len(root):].lstrip('/')
    return value

# Register the custom filters
app.jinja_env.filters['regex_match'] = regex_match
app.jinja_env.filters['remove_duplicate_root'] = remove_duplicate_root

def process_form(label_data, magnet_data):
    logging.info("Starting Torrent Download")
    subprocess.run(["/usr/bin/python3", "/etc/python-web-server/download_torrent.py", label_data, magnet_data])
    # Custom function to process the form data
    # Implement your desired functionality here
    logging.info(f"Form data: {label_data} {magnet_data}")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
