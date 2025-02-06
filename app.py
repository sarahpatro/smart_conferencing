from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from your_mom_script import generate_mom  # Extracts MoM from file
from email import send_email_with_attachment  # Sends summary to participants
from chatbot import list_files, change_directory, read_file, agent  # Imports chatbot functions

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

    # Generate MoM
    mom_text = generate_mom(file_path)

    # Send summary via email
    send_email_with_attachment (mom_text)

    return jsonify({"mom": mom_text})


@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    response = agent.run({"input": question, "chat_history": []})
    return jsonify({"answer": response})


@app.route("/files", methods=["GET"])
def list_uploaded_files():
    return jsonify({"files": list_files(UPLOAD_FOLDER)})


@app.route("/change_directory", methods=["POST"])
def change_working_directory():
    data = request.get_json()
    path = data.get("path")
    if not path:
        return jsonify({"error": "No path provided"}), 400

    return jsonify({"message": change_directory(path)})


@app.route("/read_file", methods=["POST"])
def read_uploaded_file():
    data = request.get_json()
    file_path = data.get("file_path")
    if not file_path:
        return jsonify({"error": "No file path provided"}), 400

    return jsonify({"content": read_file(file_path)})


if __name__ == "__main__":
    app.run(debug=True)
