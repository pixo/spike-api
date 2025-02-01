from flask import Flask, request, jsonify
import dropbox
import os

app = Flask(__name__)


# 🔥 Charger l'Access Token depuis cred.txt
def load_access_token():
    try:
        with open("cred.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("⚠️ ERREUR: cred.txt introuvable !")
        return None


ACCESS_TOKEN = load_access_token()
if not ACCESS_TOKEN:
    raise ValueError("❌ Aucun Access Token trouvé. Ajoutez votre token dans cred.txt.")

dbx = dropbox.Dropbox(ACCESS_TOKEN)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Reçoit un fichier via API et l'upload vers Dropbox."""
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier trouvé"}), 400

    file = request.files['file']
    dropbox_path = f"/harmonia/{file.filename}"

    dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode("overwrite"))

    return jsonify({"message": f"✅ Fichier {file.filename} uploadé avec succès sur Dropbox."})


@app.route('/download', methods=['GET'])
def download_file():
    """Télécharge un fichier depuis Dropbox et le renvoie."""
    file_name = request.args.get('filename')

    if not file_name:
        return jsonify({"error": "Nom du fichier requis"}), 400

    dropbox_path = f"/harmonia/{file_name}"
    local_path = f"./{file_name}"

    dbx.files_download_to_file(local_path, dropbox_path)

    return jsonify({"message": f"📥 Fichier {file_name} téléchargé avec succès."})


@app.route('/list', methods=['GET'])
def list_files():
    """Liste les fichiers disponibles dans le dossier Dropbox."""
    try:
        files = dbx.files_list_folder("/harmonia").entries
        file_names = [file.name for file in files]
        return jsonify({"files": file_names})
    except dropbox.exceptions.ApiError:
        return jsonify({"error": "Impossible d'accéder au dossier."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)