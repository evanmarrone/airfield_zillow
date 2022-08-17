import googlemaps
from datetime import datetime
import time
import pandas as pd
import numpy as np

api_key = 'AIzaSyBXScMzId9sFeej9IX45M_vVBO6KpoC6LE'
gmaps = googlemaps.Client(key=api_key)



class Airfield():
    
    def __init__(self, name, country, location, radius=5):
        self.location = location
        self.country = country
        self.name = name
        self.radius = radius
        
    def place_search(self, location, radius, location_type):
        places_result = gmaps.places_nearby(location = location, radius = radius, type = location_type)
        time.sleep(3)
        try:
            places_result2 = gmaps.places_nearby(page_token = places_result["next_page_token"])
            places_result["results"].extend(places_result2["results"])
            time.sleep(3)
        except:
            places_result2 = None
        try:
            places_result3 = gmaps.places_nearby(page_token = places_result2["next_page_token"])
            places_result["results"].extend((places_result3["results"]))
        except:
            places_result2 = None
        return places_result["results"]
    
    
    def search_number_in_prox(self, location_type, distance=5):
        distance /= 0.000621371  # converts meters to miles
        locations = self.place_search(self.location, distance, location_type)
        number_close = len(locations)
        return number_close
    
    
    def createDF(self):
        self.lodging = self.search_number_in_prox("lodging")
        self.contractors = self.search_number_in_prox("hardware_store")
        self.restaurants = self.search_number_in_prox("restaurant")
        self.hospitals = self.search_number_in_prox("hospital")
        
        data = [[self.name, self.country, self.lodging, self.contractors, self.restaurants, self.hospitals]]
        self.df = pd.DataFrame(data, columns=["Airfield Name", "Country", 'Lodging',"Contractors","Restaurants","Hospitals"])
        
        
    def search(self, location_type, distance=5):
        distance /= 0.000621371  # miles
        locations = self.place_search(self.location, distance, location_type)
        resultsDF = pd.DataFrame.from_dict(locations)
        try:
            ave_rating = round(resultsDF.rating.mean(),1)
        except:
            ave_rating = "NaN"
        number_close = len(resultsDF)
        return location_type, ave_rating, number_close
        
        
    def createSummaryDF(self):
        
        # initialize list of lists
        lodging = self.search("lodging")
        contractors = self.search("hardware_store")
        restaurants = self.search("restaurant")
        hospitals = self.search("hospital")
        
        data = [lodging,contractors,restaurants,hospitals]
          
        # Create the pandas DataFrame
        self.summaryDF = pd.DataFrame(data, columns=['Category', 'Average Rating', "Number of Category in X Miles".format(self.radius)])