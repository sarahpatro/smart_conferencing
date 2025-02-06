from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from your_mom_script import generate_mom  # Import your function

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")  # Serve frontend


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # Call your MoM extraction function
    mom_text = generate_mom(file_path)  # Ensure `generate_mom` exists in your script

    return jsonify({"mom": mom_text})


if __name__ == "__main__":
    app.run(debug=True)
