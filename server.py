from flask import Flask, request, jsonify
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import os
from googleapiclient.http import MediaIoBaseUpload
import io

app = Flask(__name__)

# Charger les credentials
CREDENTIALS_FILE = "spike_anarchiste.json"
creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=["https://www.googleapis.com/auth/drive"])

# Initialisation du client Google Drive
service = build('drive', 'v3', credentials=creds)

@app.route('/list_files', methods=['GET'])
def list_files():
    """Liste les fichiers du Google Drive"""
    results = service.files().list().execute()
    files = results.get('files', [])
    return jsonify(files)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """Upload un fichier sur Google Drive"""
    file = request.files['file']
    file_metadata = {'name': file.filename}
    media = MediaIoBaseUpload(file, mimetype=file.content_type)
    uploaded_file = service.files().create(body=file_metadata, media_body=media).execute()
    return jsonify({"fileId": uploaded_file.get("id")})

@app.route('/download_file', methods=['GET'])
def download_file():
    """Télécharge un fichier depuis Google Drive"""
    file_id = request.args.get('file_id')
    request_drive = service.files().get_media(fileId=file_id)
    return request_drive.execute()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)