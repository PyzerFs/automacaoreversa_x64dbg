from flask import Flask, request, render_template, send_from_directory, redirect, url_for # type: ignore
import os, hashlib, datetime
from weasyprint import HTML # type: ignore

BASE_UPLOAD = "dumps"
REPORT_FOLDER = "reports"
os.makedirs(BASE_UPLOAD, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

app = Flask(__name__)


# --- Gerar hash SHA256 do arquivo ---
def get_file_hash(file_stream):
    h = hashlib.sha256()
    file_stream.seek(0)
    h.update(file_stream.read())
    file_stream.seek(0)
    return h.hexdigest()


# --- Upload de arquivos ---
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    file_hash = get_file_hash(file)
    folder = os.path.join(BASE_UPLOAD, file_hash)
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file.save(os.path.join(folder, filename))
    return "Uploaded", 200


# --- Página principal ---
@app.route("/")
def index():
    hashes = os.listdir(BASE_UPLOAD)
    data = []
    for h in hashes:
        folder = os.path.join(BASE_UPLOAD, h)
        files = os.listdir(folder)
        data.append({'hash': h, 'files': files, 'count': len(files)})
    return render_template("index.html", data=data)


# --- Visualizar arquivos de um hash ---
@app.route("/view/<file_hash>")
def view_dump(file_hash):
    folder = os.path.join(BASE_UPLOAD, file_hash)
    if not os.path.exists(folder):
        return "Hash não encontrado", 404
    files = os.listdir(folder)
    # Classificar por tipo: regs, mem, stack
    regs_files = [f for f in files if "regs" in f]
    mem_files = [f for f in files if "mem" in f]
    stack_files = [f for f in files if "stack" in f]
    return render_template("view_dump.html", hash=file_hash, regs=regs_files, mem=mem_files, stack=stack_files)


# --- Comparar múltiplos testes ---
@app.route("/compare/<file_hash>")
def compare(file_hash):
    folder = os.path.join(BASE_UPLOAD, file_hash)
    if not os.path.exists(folder):
        return "Hash não encontrado", 404
    files = os.listdir(folder)
    return render_template("compare.html", hash=file_hash, files=files)


# --- Download individual ---
@app.route("/download/<file_hash>/<filename>")
def download_file(file_hash, filename):
    folder = os.path.join(BASE_UPLOAD, file_hash)
    return send_from_directory(folder, filename, as_attachment=True)


# --- Gerar relatório PDF completo ---
@app.route("/report_pdf/<file_hash>")
def report_pdf(file_hash):
    folder = os.path.join(BASE_UPLOAD, file_hash)
    if not os.path.exists(folder):
        return "Hash não encontrado", 404
    files = os.listdir(folder)
    html_content = render_template("view_dump.html", hash=file_hash, regs=[f for f in files if "regs" in f],
                                   mem=[f for f in files if "mem" in f],
                                   stack=[f for f in files if "stack" in f])
    pdf_file = os.path.join(REPORT_FOLDER, f"{file_hash}.pdf")
    HTML(string=html_content).write_pdf(pdf_file)
    return send_from_directory(REPORT_FOLDER, f"{file_hash}.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
