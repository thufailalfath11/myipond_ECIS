import subprocess
import base64
import binascii
import json
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, db
from flask_cors import CORS

# 🔹 Kunci AES-256 dan IV (SAMA dengan yang dipakai untuk enkripsi)
key = b'12345678901234567890123456789012'  # 32-byte key
iv = b'1234567890123456'  # 16-byte IV

# Konversi kunci dan IV ke HEX
key_hex = binascii.hexlify(key).decode()
iv_hex = binascii.hexlify(iv).decode()

# 🔹 Inisialisasi Firebase
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://dummyecis-default-rtdb.firebaseio.com/"
})

app = Flask(__name__)
CORS(app)
def decrypt_aes_openssl(encrypted_b64):
    """Dekripsi data menggunakan OpenSSL AES-256-CBC"""
    try:
        # Decode Base64 ke biner
        encrypted_data = base64.b64decode(encrypted_b64)

        # Simpan ke file sementara
        with open('encrypted.bin', 'wb') as enc_file:
            enc_file.write(encrypted_data)

        # Dekripsi dengan OpenSSL
        command = (
            f"openssl enc -aes-256-cbc -pbkdf2 -d -K {key_hex} -iv {iv_hex} "
            f"-in encrypted.bin -out decrypted.txt"
        )
        subprocess.run(command, shell=True, check=True)

        # Baca hasil dekripsi
        with open('decrypted.txt', 'r') as dec_file:
            decrypted_data = dec_file.read()

        # Hapus file sementara
        subprocess.run("rm -f encrypted.bin decrypted.txt", shell=True)

        return decrypted_data

    except Exception as e:
        print(f"❌ Error decrypting: {e}")
        return None

@app.route('/decrypt-data', methods=['GET'])
def decrypt_data():
    try:
        # Ambil data terakhir dari Firebase
        ref = db.reference("/encrypted_data")
        encrypted_entries = ref.get()

        if not encrypted_entries:
            return jsonify({"error": "No encrypted data found in Firebase"}), 404

        # Ambil satu data terakhir
        last_key = list(encrypted_entries.keys())[-1]
        encrypted_b64 = encrypted_entries[last_key]["data"]

        print(f"🔹 Encrypted Data: {encrypted_b64}")

        # Dekripsi data
        decrypted_json = decrypt_aes_openssl(encrypted_b64)

        if decrypted_json:
            print(f"✅ Decrypted Data: {decrypted_json}")
            return jsonify({"decrypted": json.loads(decrypted_json)})
        else:
            return jsonify({"error": "Failed to decrypt data"}), 500

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
