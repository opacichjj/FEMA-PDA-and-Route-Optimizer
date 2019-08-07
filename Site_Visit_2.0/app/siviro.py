from app.api_keys import google_key, zillow_key
import googlemaps
import zillow
import requests
from app.address import *

# Sight Visit Route OPtimization

# loops through a list of addresses given by user
def prompt_address(origin, web_dicta, final_destination):

    address_list = []
    """origin = get_origin()"""
    address_list.append(origin)
    # list comprehension to unpack dictionary
    multi_address = [web_dicta[key] for key in web_dicta]
    address_list.extend(multi_address)

    # append address_list with final_destination
    """#final_destination = prompt_round_trip(origin)"""
    address_list.extend(final_destination)

    # optimizes the addresses list
    address_list = get_optimized(address_list)
    # converts list to list of coordinates
    coord_list = convert_list_latlng(address_list)
    #
    route_url = get_directions_url(coord_list)

    return route_url


# converts address to lat and lng
# returns tuple
def convert_to_latlng(address):

    gmaps = googlemaps.Client(key=google_key)
    geocode = gmaps.geocode(address)
    lat = geocode[0]['geometry']['location']['lat']
    lng = geocode[0]['geometry']['location']['lng']
    return (lat, lng)


# takes in list and unpacks tuple coordinate
# returns a list
def convert_list_latlng(list_of_address):

    converted_latlng  = []
    for address in list_of_address:
        converted_latlng.append(convert_to_latlng(address))
    return converted_latlng


# optimizes the list of addresses using google
# returns list in correct order
def get_optimized(list_of_addresses):

    gmaps = googlemaps.Client(key=google_key)
    route = gmaps.directions(origin=list_of_addresses[0],
                            destination=list_of_addresses[-1],
                            mode='driving',
                            waypoints=list(list_of_addresses[1:-1]),
                            optimize_waypoints=True)
    route[0]['waypoint_order']
    opt_route = route[0]['waypoint_order']
    opt_route = [i+1 for i in opt_route]
    opt_route = [0]+opt_route+[-1]
    route = [opt_route[i] for i in opt_route]
    optimized_list = []
    for i in route:
        optimized_list.append(list_of_addresses[i])
    return optimized_list
    return list_of_addresses


# takes in converted list of optimzed routes
# returns str url for google maps
def get_directions_url(list_of_coords):

    url = 'https://www.google.com/maps/dir/'
    for i in range(len(list_of_coords)):
        lat, lng = list_of_coords[i]
        url += str(lat) + ',' + str(lng) + '/'
    return url


"""  All code below is not used at this point, delete unnecessary code and detail comments on any potentially useful code"""

"""
unused code from previous versions of siviro to handle erorrs
it originally belonged to the 'prompt_address' function
may need to incorporate this

# exits loop when users types 'exit'
# type 'test' for a premade list
# returns a list of addresses
stay_in_loop = True
while stay_in_loop:
    response = input("Please enter address or type 'exit': ")
    if response == 'exit':
        stay_in_loop = False
        break
    if response == 'test':
        test_list = get_test_list()
        for address in test_list:
            formatted_address = get_formal_address(address)
            address_list.append(formatted_address)
        stay_in_loop = False
        break
    else:
        try:
            response = get_formal_address(response)
            address_list.append(response)
        except:
            print("Invalid address")
"""
