from flask import Flask, request, send_from_directory, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    files = os.listdir(UPLOAD_FOLDER)
    html = """
    <h1>📤 DevOps File Sharing Microservice</h1>
    <p><strong>Upload from Mobile → View on Tab</strong></p>
    <form method="post" enctype="multipart/form-data" action="/upload">
        <input type="file" name="file">
        <input type="submit" value="Upload File">
    </form>
    <h2>Uploaded Files (accessible on any device):</h2>
    <ul>
    """ + "".join([f'<li>{f} <a href="/download/{f}">Download</a></li>' for f in files]) + "</ul>"
    return render_template_string(html)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return f"✅ File '{file.filename}' uploaded successfully! Refresh on other device."

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
