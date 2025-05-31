from flask import Flask, jsonify
import subprocess
import firebase_admin
from firebase_admin import credentials, db
import binascii
import json
from flask_cors import CORS

# 🔹 Setup Firebase
cred = credentials.Certificate("firebase-key.json")  # Ganti path sesuai file kamu
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://ecis-database-default-rtdb.firebaseio.com"
})

key = b'12345678901234567890123456789012'  # 32-byte key
iv = b'1234567890123456'  # 16-byte IV

app = Flask(__name__)
CORS(app)

def decrypt_aes_openssl(encrypted_base64):
    with open('encrypted.bin', 'w') as enc_file:
        enc_file.write(encrypted_base64)
    command = (
        f"openssl enc -aes-256-cbc -pbkdf2 -d -base64 -K {binascii.hexlify(key).decode()} -iv {binascii.hexlify(iv).decode()} "
        f"-in encrypted.bin -out decrypted.txt"
    )
    subprocess.run(command, shell=True, check=True)
    with open('decrypted.txt', 'r') as dec_file:
        decrypted_data = dec_file.read()
    subprocess.run("rm -f encrypted.bin decrypted.txt", shell=True)
    return decrypted_data


@app.route('/decrypt-data', methods=['GET'])
def decrypt_data():
    try:
        ref = db.reference("/encrypted_data")
        all_dates = ref.get()
        if not all_dates:
            return jsonify({"error": "No encrypted data found in Firebase."}), 404

        # Ambil tanggal terbaru (format: YYYY-MM-DD)
        date_keys = sorted(all_dates.keys())
        latest_date = date_keys[-1]
        daily_data = all_dates[latest_date]
        if not daily_data:
            return jsonify({"error": f"No data found for date {latest_date}."}), 404

        # Ambil pushkey terakhir pada tanggal terbaru
        push_keys = sorted(daily_data.keys())
        last_push_key = push_keys[-1]
        encrypted_text = daily_data[last_push_key]["data"]

        decrypted_text = decrypt_aes_openssl(encrypted_text)
        decrypted_json = json.loads(decrypted_text)

        return jsonify({
            "date": latest_date,
            "decrypted_data": decrypted_json
        })

    except Exception as e:
        print(f"❌ Error in decrypt_data: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8443, debug=True)
