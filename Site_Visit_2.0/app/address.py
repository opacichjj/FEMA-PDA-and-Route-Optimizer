from app.api_keys import *
import googlemaps
import zillow
import requests
import os

from urllib.parse import quote_plus
from urllib.request import urlretrieve
# from geopy import geocoders

# creates an Address object
class Address:
    # raw_address is a google search query (zip or city should be included at minimum)
    def __init__(self, raw_address):
        self.raw_address = raw_address
        self.lat = None
        self.lng = None
        self.street_number = None
        self.street_name = None
        self.city_name = None
        self.state_abr = None
        self.postal_code = None
        self.formatted_address = None
        self.google_place_id = None
        self.street_pic = None
        self.zillow_estimate = None
        self.zillow_baths = None
        self.zillow_bedrooms = None
        # self.applicant_estimate = ""
        # self.type_of_insurance = ""
        # self.level_of_damage = ""


        # sets the attributes
        self.set_google_coords()
        self.set_zillow()
        self.set_google_street_pic()

    # uses gmaps api for housing location
    def set_google_coords(self):
        # instantiate gmaps object
        gmaps = googlemaps.Client(key=google_key)
        geocode = gmaps.geocode(self.raw_address)

        # set values for housing location
        self.lat = geocode[0]['geometry']['location']['lat']
        self.lng = geocode[0]['geometry']['location']['lng']
        self.google_place_id = geocode[0]['place_id']
        self.formatted_address = geocode[0]['formatted_address']
        # loops for every item in address_components
        for i in geocode[0]['address_components']:
            if(i['types'] == ['street_number']):
                self.street_number = i['long_name']
            if(i['types'] == ['route']):
                self.street_name = i['long_name']
            if(i['types'] == ['locality', 'political']):
                self.city_name = i['long_name']
            if(i['types'] == ['administrative_area_level_1', 'political']):
                self.state_abr = i['short_name']
            if(i['types'] == ['postal_code']):
                self.postal_code = i['short_name']


    # uses zillow api
    # adapted code from DSI-DC-6
    def set_zillow(self):
        zillow_api = zillow.ValuationApi()
        house = f'{self.street_number} {self.street_name}'

        # estimate int, baths str, bedrooms str
        try:
            house_data = zillow_api.GetDeepSearchResults(zillow_key, house, self.postal_code)
            self.zillow_estimate = house_data.zestimate.amount
            self.zillow_baths = house_data.extended_data.bathrooms
            self.zillow_bedrooms = house_data.extended_data.bedrooms
        #Error if zillow doesnt have price for property
        except:
            print('Zillow does not have price for this address')


    # uses google street view static api
    # adapted from DSI-DC-6
    def set_google_street_pic(self, save_loc=r"./app/images/"):
        image_url = f'https://maps.googleapis.com/maps/api/streetview?size=600x600&location={self.lat},{self.lng}&key={google_key}'
        pic_file_name = f'{self.google_place_id}.google.jpeg'

        # saves picture in images folder
        urlretrieve(image_url, os.path.join(save_loc, pic_file_name))
        # sets Addreses.street_pic to file path
        self.street_pic = pic_file_name

    # returns image url for static picture
    def get_google_street_pic(self):
        image_url = f'https://maps.googleapis.com/maps/api/streetview?size=600x600&location={self.lat},{self.lng}&key={google_key}'
        return image_url

    # useful method for debugging
    # returns a diction of attributes
    def show(self):
        dict = {
            'lat' : self.lat,
            'lng' : self.lng,
            'street_number' : self.street_number,
            'street_name' : self.street_name,
            'city_name' : self.city_name,
            'state_abr' : self.state_abr,
            'postal_code' : self.postal_code,
            'formatted_address' : self.formatted_address,
            'google_place_id' : self.google_place_id,
            'zillow_estimate' : self.zillow_estimate,
            'zillow_baths' : self.zillow_baths,
            'zillow_bedrooms' : self.zillow_bedrooms
            }
        return dict


# need to convert to unique id to save in database
def get_address_id(address_query):
    address_object = Address(address_query)
    id = address_object.google_place_id
    return id


#  uses google distance matrix api
def calculate_distance(address1, address2):
    pass


def get_list_of_addresses():
    pass


# reutrns url for any number of addresses
def get_directions_url(list_of_address):
    url = 'https://www.google.com/maps/dir/'
    for address in list_of_address:
        url += str(address.lat) + ',' + str(address.lng) + '/'
    return url


"""
uncomment for debugging
my_address = Address("313 Elm St NW, Washington, DC 20001")
my_address.street_pic
my_address.show()
"""
