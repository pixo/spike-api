from flask import Flask, request, jsonify
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

# Config GitHub (à modifier avec tes infos)
GITHUB_REPO = "git@github.com:pixo/spike.git"  # ⚠️ Vérifie l'URL SSH si besoin
GIT_BRANCH = "main"  # Branche où pousser les commits

# Dossier où seront enregistrés les fichiers
BASE_DIR = "/app/repository"

# Assure-toi que le dossier existe
os.makedirs(BASE_DIR, exist_ok=True)


@app.route("/", methods=["GET"])
def home():
    return "🚀 Harmonia Commit API is running!", 200


@app.route("/commit", methods=["POST"])
def commit_code():
    """
    Reçoit du code via POST, l'enregistre et fait un commit + push.
    """
    data = request.get_json()

    if not data or "filename" not in data or "content" not in data:
        return jsonify({"error": "Requête invalide. Il faut 'filename' et 'content'."}), 400

    filename = data["filename"]
    content = data["content"]

    file_path = os.path.join(BASE_DIR, filename)

    try:
        # 🔹 Écriture du fichier
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 🔹 Commit + Push
        commit_message = f"Update {filename} - {datetime.now().isoformat()}"
        subprocess.run(["git", "-C", BASE_DIR, "add", filename], check=True)
        subprocess.run(["git", "-C", BASE_DIR, "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "-C", BASE_DIR, "push", "origin", GIT_BRANCH], check=True)

        return jsonify({"message": f"{filename} enregistré et commité avec succès !"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
