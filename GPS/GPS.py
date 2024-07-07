import requests
import time
import json

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64encode

def encrypt_data(data, key, iv):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_data = data + (16 - len(data) % 16) * chr(16 - len(data) % 16)
    encrypted_data = encryptor.update(padded_data.encode('utf-8')) + encryptor.finalize()
    return b64encode(encrypted_data).decode('utf-8')

key = b'1234567890123456'  
iv = b'1234567890123456' 

with open('backend/geo_data/Car_Path.txt', 'r') as file:
    lines = file.readlines()

coords = []

for index,line in enumerate(lines):
    if index<180:
        continue
    line = line.strip()
    lon, lat = map(float, line.split(','))
    coords.append([lon,lat])

coords.append([1, 1])

print("sending coordinates: --")

server_url = 'http://localhost:5000/gps'
frontend_url='http://localhost:4000/gps'

for index,coord in enumerate(coords):
    data = {
        'latitude': coord[1],
        'longitude': coord[0]
    }
    encrypted_data = encrypt_data(json.dumps(data), key, iv)

    response_server = requests.post(server_url, json={'encrypted_data': encrypted_data})
    print(response_server.json(),index+1)
    frontend_data={
        'latitude': coord[1],
        'longitude': coord[0],
        'distance': response_server.json()['distance']
    }
    encrypted_data = encrypt_data(json.dumps(frontend_data), key, iv)
    response_frontend = requests.post(frontend_url, json={'encrypted_data': encrypted_data})
    time.sleep(1)

time.sleep(5)

print("Server process finished....")

url = 'http://localhost:5000/shutdown'
response = requests.get(url)
print(response.json())
  
time.sleep(1)
print("server closed")