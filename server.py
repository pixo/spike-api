from flask import Flask, request, jsonify, abort
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

# Config GitHub (à modifier avec tes infos)
GITHUB_REPO = "git@github.com:pixo/spike.git"
GIT_BRANCH = "main"
BASE_DIR = "/app/repository"
os.makedirs(BASE_DIR, exist_ok=True)

# Token d'authentification pour sécuriser l'accès (exemple, à modifier)
API_TOKEN = "ton_token_secret"

@app.get("/check-git")
def check_git():
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        return {"message": result.stdout.strip()}
    except FileNotFoundError:
        return {"error": "Git is not installed on the server."}

@app.route("/", methods=["GET"])
def home():
    return "🚀 Harmonia Commit API is running!", 200

@app.route("/commit", methods=["POST"])
def commit_code():
    # Vérification du token d'authentification
    token = request.headers.get("Authorization")
    if token != f"Bearer {API_TOKEN}":
        abort(401, "Unauthorized")

    data = request.get_json()
    if not data or "filename" not in data or "content" not in data:
        return jsonify({"error": "Requête invalide. Il faut 'filename' et 'content'."}), 400

    filename = data["filename"]
    content = data["content"]
    file_path = os.path.join(BASE_DIR, filename)

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        commit_message = f"Update {filename} - {datetime.now().isoformat()}"
        subprocess.run(["git", "-C", BASE_DIR, "add", filename], check=True, capture_output=True, text=True)
        subprocess.run(["git", "-C", BASE_DIR, "commit", "-m", commit_message], check=True, capture_output=True, text=True)
        subprocess.run(["git", "-C", BASE_DIR, "push", "origin", GIT_BRANCH], check=True, capture_output=True, text=True)

        return jsonify({"message": f"{filename} enregistré et commité avec succès !"}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": f"Erreur Git: {e.stderr}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
