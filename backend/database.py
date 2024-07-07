from class_defination import Organizer # type: ignore

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class MongoDBManager:
    def __init__(self, uri, db_name):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None 

    def start_connection(self):
        try:
            self.client = MongoClient(self.uri)
            self.db = self.client[self.db_name]
            print("Connected to MongoDB Atlas")
        except ConnectionFailure as e:
            print(f"Could not connect to MongoDB Atlas: {e}")

    def end_connection(self):
        if self.client:
            self.client.close()
            print("Connection to MongoDB Atlas closed")

    def retrieve_data(self, collection_name, query):
        collection = self.db[collection_name] # type: ignore
        return collection.find(query)

    def update_data(self, collection_name, query, new_values):
        collection = self.db[collection_name] # type: ignore
        updated_doc = collection.update_one(query, {"$set": new_values})
        return updated_doc.modified_count


uri = "mongodb+srv://anshammaurya2291:ansham123@cluster1.qyllrbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"
db_name = "GPSBasedTollSimulation"


mongo_manager = MongoDBManager(uri, db_name)
mongo_manager.start_connection()

vehical_data={}
for user in mongo_manager.retrieve_data("user_info", {"toll_tag_id":"IND1D992835625UUO27A"}):
    vehical_data=user


points_geojson = 'backend/geo_data/INDIA_NATIONAL_HIGHWAY.geojson'
zones_geojson = 'backend/geo_data/square_zone.geojson' 

org=Organizer(vehical_data['car_plate_no'])
nationalHighways = org.load_national_highways(points_geojson)
tollZones = org.load_toll_zones(zones_geojson)


