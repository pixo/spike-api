import subprocess
import os
from datetime import datetime
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# 🔑 Token de sécurité pour éviter les requêtes externes
API_TOKEN = "ton_token_secret"

# 📂 Chemin du repo Git
GIT_REPO_PATH = "/app/spike"


@app.route("/", methods=["GET"])
def home():
    return "🚀 Harmonia Commit API is running!", 200


@app.route("/push_code", methods=["POST"])
def push_code():
    """ Reçoit du code, l'écrit dans un fichier et fait un commit + push """

    token = request.headers.get("Authorization")
    if token != f"Bearer {API_TOKEN}":
        abort(401, "Unauthorized")

    data = request.get_json()
    if not data or "filename" not in data or "content" not in data:
        return jsonify({"error": "Requête invalide. Il faut 'filename' et 'content'."}), 400

    filename = data["filename"]
    content = data["content"]
    file_path = os.path.join(GIT_REPO_PATH, filename)

    try:
        # 📄 Écriture du fichier avec le contenu reçu
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 📝 Ajout à Git, commit et push
        commit_message = f"Update {filename} - {datetime.now().isoformat()}"
        subprocess.run(["git", "-C", GIT_REPO_PATH, "add", "."], check=True)
        subprocess.run(["git", "-C", GIT_REPO_PATH, "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "-C", GIT_REPO_PATH, "push"], check=True)

        return jsonify({"message": f"{filename} mis à jour et pushé avec succès !"}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Erreur Git: {e.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)