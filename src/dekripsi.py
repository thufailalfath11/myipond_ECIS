from flask import Flask, request, jsonify
import subprocess
import base64
import firebase_admin
from firebase_admin import credentials, db
import binascii
import json
from flask_cors import CORS  # 🔹 Tambahkan ini



# 🔹 Setup Firebase
cred = credentials.Certificate("firebase-key.json")  # Sesuaikan dengan path
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://ecisdata-ae40e-default-rtdb.firebaeio.com/"
})

# 🔹 Kunci AES-256 dan IV (HARUS sama dengan yang digunakan untuk enkripsi)
key = b'12345678901234567890123456789012'  # 32-byte key
iv = b'1234567890123456'  # 16-byte IV

# Konversi kunci dan IV ke HEX untuk OpenSSL
def decrypt_aes_openssl(encrypted_base64):
    """Dekripsi data menggunakan OpenSSL AES-256-CBC"""
    # Decode dari base64 ke binary
    encrypted_data = base64.b64decode(encrypted_base64)
    
    # Simpan data terenkripsi ke file sementara
    with open('encrypted.bin', 'wb') as enc_file:
        enc_file.write(encrypted_data)
    
    # Dekripsi dengan OpenSSL
    command = (
        f"openssl enc -aes-256-cbc -pbkdf2 -d -base64 -K {binascii.hexlify(key).decode()} -iv {binascii.hexlify(iv).decode()} "
        f"-in encrypted.bin -out decrypted.txt"
    )
    subprocess.run(command, shell=True, check=True)
    
    # Baca hasil dekripsi
    with open('decrypted.txt', 'r') as dec_file:
        decrypted_data = dec_file.read()
    
    # Hapus file sementara
    subprocess.run("rm -f encrypted.bin decrypted.txt", shell=True)
    
    return decrypted_data

app = Flask(__name__)
CORS(app)  # 🔹 Aktifkan CORS untuk semua endpoint
@app.route('/decrypt-data', methods=['GET'])
def decrypt_data():
    try:
        # Ambil data terakhir dari Firebase
        ref = db.reference("/encrypted_data")
        encrypted_entries = ref.get()
        
        print(f"🔍 Data Firebase: {encrypted_entries}")  # Debug log

        if not encrypted_entries:
            return jsonify({"error": "No encrypted data found in Firebase."}), 404
        
        # Ambil data terakhir
        last_key = list(encrypted_entries.keys())[-1]
        encrypted_text = encrypted_entries[last_key]["data"]
        
        print(f"🔑 Encrypted Data: {encrypted_text}")  # Debug log

        decrypted_text = decrypt_aes_openssl(encrypted_text)
        
        print(f"🔓 Decrypted Text: {decrypted_text}")  # Debug log

        # Parse hasil dekripsi ke JSON
        decrypted_json = json.loads(decrypted_text)
        
        return jsonify({"decrypted_data": decrypted_json})

    except Exception as e:
        print(f"❌ Error in decrypt_data: {e}")  # Debug log
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, debug=True)
