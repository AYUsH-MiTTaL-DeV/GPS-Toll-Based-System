from shapely.geometry import Point, LineString
import geopandas as gpd
import requests

class Entity:
    def __init__(self, plate_no):
        self.plate_no = plate_no

        self.distance_travelled = 0
        self.zone_wise_distance = 0

        self.coordinates = CoordinateList(self) 

    def update_distance(self, previous, current):
        url = f'http://router.project-osrm.org/route/v1/driving/{previous};{current}'
        params = {
            'overview': 'full',
            'geometries': 'geojson'
        }
        response = requests.get(url, params=params)
        directions = response.json()

        if directions['code'] == 'Ok':
            distance = directions['routes'][0]['distance'] / 1000
            self.distance_travelled += distance
            self.zone_wise_distance += distance
        else:
            raise Exception('Error fetching directions: {}'.format(directions['code']))

class CoordinateList:
    def __init__(self, entity):
        self.coordinates = []
        self.entity = entity

    def append(self, coordinate):
        if self.coordinates:
            previous = self.coordinates[-1]
            self.entity.update_distance(previous, coordinate)
        self.coordinates.append(coordinate)

    def clear(self):
        self.coordinates = []

class Organizer:
    def __init__(self,entity_info):
        self.entity = Entity(entity_info)
        self.envoices = []

    def zone_wise_distance_toll_collection(self,tax_rate=1):
        tax_reduction = self.entity.zone_wise_distance * tax_rate
        if tax_reduction==0:
            return False
        envoice=(f"Entity with plate no {self.entity.plate_no} "
                     f"traveled {self.entity.zone_wise_distance:.2f} km with tax reduction {tax_reduction:.2f}.")
        self.envoices.append([envoice,tax_reduction])
        return True
    
    def total_toll_collection(self):
        total_toll_deducted=0
        for envoice in self.envoices:
            total_toll_deducted+=envoice[1]
        
        return [total_toll_deducted, f"Total toll tax collected from Entity user with plate no {self.entity.plate_no} is {total_toll_deducted:.3f}."]

    @staticmethod
    def load_national_highways(roads_geojson):
        gdf = gpd.read_file(roads_geojson)
        national_highways = []
        for index, row in gdf.iterrows():
            if row.geometry.geom_type == 'LineString':
                highway = row.geometry
                nh_no = row['NH_No']
                national_highways.append((nh_no, highway))
        return national_highways
    
    @staticmethod
    def load_toll_zones(zones_geojson):
        gdf = gpd.read_file(zones_geojson)
        toll_zones = []
        for index, row in gdf.iterrows():
            if row['geometry'].geom_type == 'Polygon' or row['geometry'].geom_type == 'MultiPolygon':
                polygon = row['geometry']
                name = row['NAME_1']
                price= row['PRICE']
                toll_zones.append((name,price,polygon))
        return toll_zones

    def is_vehicle_on_any_toll_road(self,vehicle_position, nationalHighways, buffer_distance_meters=5):
        for name,highway_coords in nationalHighways:
            highway_line = LineString(highway_coords)
            point = Point(vehicle_position)
            highway_buffer = highway_line.buffer(buffer_distance_meters / 111139)
            if  highway_buffer.contains(point):
                return [True,name]
        return [False]

    def return_toll_zone_and_tax_rate(self,vehicle_position, toll_zones):
        vehicle_point = Point(vehicle_position[0],vehicle_position[1])
        for name,price,toll_zone in toll_zones:
            if toll_zone.contains(vehicle_point):
                return [True,name,price]
        return [False,None,1]