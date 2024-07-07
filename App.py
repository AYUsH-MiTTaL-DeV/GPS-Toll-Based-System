#if using vertual environment attach your python.exe path to the frontend and backend veriable
import subprocess
import time

frontend = subprocess.Popen(['Scripts/python.exe', 'frontend/frontend.py'])
backend = subprocess.Popen(['Scripts/python.exe', 'backend/flask_server.py'])

time.sleep(15)

run_application = subprocess.Popen(['Scripts/python.exe', 'GPS/GPS.py'])


#if not using the vertual environment----
#dont run the app.py
#run the three py script seperately in different terminals--frontend,backend,GPS
#important
#run these script from base folder only to avoid path errors
#python frontend/frontend.py
#python backend/flask_server.py
#python GPS/GPS.py
