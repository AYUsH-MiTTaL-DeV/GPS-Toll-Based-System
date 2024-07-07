# Vehicle Toll Tracking System and GPS Toll Collection System

## Overview
This project is a vehicle toll tracking system that uses GPS coordinates to determine if a vehicle is on a toll road. The system integrates with a REST API, processes GPS data, and calculates toll fees based on the vehicle's distance traveled on toll roads.

## Features
- **Entity Tracking**: Manage vehicle information and track their travel distance.
- **GeoJSON Integration**: Load national highways and toll zones from GeoJSON files.
- **API Integration**: Use the OSRM API to calculate the distance between GPS coordinates.
- **Flask Server**: Receive GPS coordinates via a POST request and process them to check if the vehicle is on a toll road.
- **Toll Calculation**: Calculate toll fees based on the distance traveled.
- **Privacy concern**: encrypting and decrypting of data on client and server side.

## Prerequisites
- Python 3.x
- Flask
- GeoPandas/Pandas
- Requests
- Shapely
- mongoDB
- cryptocraphy

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/AYUsH-MiTTaL-DeV/GPS-Toll-Based-System
    ```
2. Navigate to the project directory:
    ```bash
    cd GPS-Toll-Based-System
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```bash
    pip install Flask GeoPandas Requests Shapely pymongo 
    ```
5. Unzip the zip file present in backend/geo_data folder:
    ```
    1.Use winrar or any other unzipping app
    2.Copy the geojson file from the unziped folder to the backend/geo_data directory i.e in the parent folder
    ```
## Usage
### Navigate to the Base directory of Project:

### 1.if using virtual environment:
### Run the App.py script:
        python App.py

### On any browser:
        localhost:4000

### --------------------------------------------------------------------------------------------------------------------
            
### 2.if not using virtual environment:
### run the frontend.py 
        python frontend/frontend.py
### run flask_server.py
        python backend/flask_server.py
### run the GPS.py
        python GPS/GPS.py
