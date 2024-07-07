from flask import Flask, request, jsonify
from database import org,tollZones,nationalHighways as NH # type: ignore
from database import mongo_manager as MM # type: ignore

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode
import json

previous_coord=[]

def payment_deduct():
    for envoice in org.envoices:
        print(envoice[0])
    output_data=org.total_toll_collection()
    print()
    print(output_data[1])

    vehical_data={}
    for user in MM.retrieve_data("user_info", {"toll_tag_id":"IND1D992835625UUO27A"}):
        vehical_data=user

    new_balance=vehical_data['bankBalance']-output_data[0]
    MM.update_data("user_info",{"car_plate_no":org.entity.plate_no},{"bankBalance":new_balance})

def car_travelling_on_toll_road(coord):
    global previous_coord

    on_road=org.is_vehicle_on_any_toll_road(coord,NH)
    zone=org.return_toll_zone_and_tax_rate(coord,tollZones)
    previous_zone=org.return_toll_zone_and_tax_rate(previous_coord,tollZones)

    if on_road[0]:
        print("car is travelling on toll road")
        if zone[1]!=previous_zone[1]:
            org.zone_wise_distance_toll_collection(previous_zone[2])
            org.entity.coordinates.clear()
            org.entity.zone_wise_distance=0
        car_coord=f'{coord[0]},{coord[1]}'
        org.entity.coordinates.append(car_coord)
    else:
        envoice=org.zone_wise_distance_toll_collection(zone[2])
        if envoice==False:
            print("car not travelling on toll road")
        else:
            payment_deduct()
            org.entity.zone_wise_distance=0
            org.entity.coordinates.clear()

    previous_coord=[coord[0],coord[1]]


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

@app.route('/gps', methods=['POST'])
def receive_gps():
    global previous_coord

    if request.is_json:
        encrypted_data = request.get_json()['encrypted_data']
        decrypted_data = decrypt_data(encrypted_data, key, iv)
    
        data = json.loads(decrypted_data)
        if data and 'latitude' in data and 'longitude' in data:
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            if previous_coord==[]:
                previous_coord=[latitude,longitude]

            print(f"Received GPS coordinates: Latitude={latitude}, Longitude={longitude}")
            car_travelling_on_toll_road([latitude,longitude])

            return jsonify({"distance": org.entity.distance_travelled}), 200
        else:
            return jsonify({"error": "Invalid coordinates"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/shutdown', methods=['GET'])
def shutdown_server():
    # payment_deduct()

    MM.end_connection()
    return jsonify({"message": "Server shutting down"}), 200
 

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
