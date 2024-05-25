from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
import requests

app = Flask(__name__)

# Configurazione del percorso di upload
UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Nessun file ricevuto'

    file = request.files['file']

    if file.filename == '':
        return 'Nessun file selezionato'

    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Invio del file al server Flask su un'altra porta
        server_url = 'http://0.0.0.0:5001/upload'  # Modifica la porta e il percorso se necessario
        files = {'file': open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'rb')}
        response = requests.post(server_url, files=files)

        return response.text

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return 'File non trovato'

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Flask in ascolto sulla porta 5000
