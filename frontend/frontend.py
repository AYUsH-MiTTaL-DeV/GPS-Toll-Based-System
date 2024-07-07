from flask import Flask, request, jsonify, render_template
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode
import json

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def decrypt_data(encrypted_data, key, iv):
    encrypted_data = b64decode(encrypted_data)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    pad_len = decrypted_padded_data[-1]
    decrypted_data = decrypted_padded_data[:-pad_len]
    return decrypted_data.decode('utf-8')


app = Flask(__name__)

key = b'1234567890123456'  
iv = b'1234567890123456'  

latest_coordinates = {"latitude": 26.769464, "longitude": 81.095838}

@app.route('/gps', methods=['POST'])
def receive_gps():
    global latest_coordinates
    global distance_travelled_in_zone

    encrypted_data = request.get_json()['encrypted_data']
    decrypted_data = decrypt_data(encrypted_data, key, iv)
    
    data = json.loads(decrypted_data)
    
    latest_coordinates = {"latitude": data['longitude'], "longitude": data['latitude'], 'distance':data['distance']}
    return jsonify({"status": "success"}), 200

@app.route('/coordinates', methods=['GET'])
def get_coordinates():
    return latest_coordinates

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
