import subprocess
import time

frontend = subprocess.Popen(['Scripts/python.exe', 'frontend/frontend.py'])
backend = subprocess.Popen(['Scripts/python.exe', 'backend/flask_server.py'])

time.sleep(15)

run_application = subprocess.Popen(['Scripts/python.exe', 'GPS/GPS.py'])
