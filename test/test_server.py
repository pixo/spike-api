import unittest
import requests
import os

# 🔥 Adresse du serveur (remplace si nécessaire)
BASE_URL = "https://spike.fly.dev"

class TestSpikeAPI(unittest.TestCase):

    def test_upload_file(self):
        """Test l'upload d'un fichier."""
        file_name = "test_file.txt"
        with open(file_name, "w") as f:
            f.write("Ceci est un test.")

        with open(file_name, "rb") as f:
            response = requests.post(f"{BASE_URL}/upload", files={"file": f})

        os.remove(file_name)  # Nettoyage après test

        self.assertEqual(response.status_code, 200)
        self.assertIn("uploadé avec succès", response.json()["message"])

    def test_list_files(self):
        """Test la récupération de la liste des fichiers."""
        response = requests.get(f"{BASE_URL}/list")
        self.assertEqual(response.status_code, 200)
        self.assertIn("files", response.json())

    def test_download_file(self):
        """Test le téléchargement d'un fichier existant."""
        file_name = "test_file.txt"
        response = requests.get(f"{BASE_URL}/download", params={"filename": file_name})

        self.assertEqual(response.status_code, 200)
        self.assertIn("téléchargé avec succès", response.json()["message"])

if __name__ == "__main__":
    unittest.main()
