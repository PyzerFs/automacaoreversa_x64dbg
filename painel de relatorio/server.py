from flask import Flask, request
import os

UPLOAD_FOLDER = "/home/user/server_dumps"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    return "Uploaded", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
