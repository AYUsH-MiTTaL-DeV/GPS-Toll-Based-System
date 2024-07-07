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
    git clone https://github.com/yourusername/GPS_Toll_Collection_System.git
    ```
2. Navigate to the project directory:
    ```bash
    cd vehicle-toll-tracking
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```bash
    pip install Flask GeoPandas Requests Shapely
    ```
5. Unzip the zip file present in geo_data folder:
   use winrar or any other unzipping app

## Usage
### Navigate to the directory:
    cd GPS_Coordinate_Sender

### Run the Application.py script:
    python Application.py

### On any browser:
    localhost:4000

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.
