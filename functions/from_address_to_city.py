import googlemaps

gmaps = googlemaps.Client(key='...')

def get_city_from_address(address):
    geocode_result = gmaps.geocode(address, language='de')
    if geocode_result:
        address_components = geocode_result[0]['address_components']
        for component in address_components:
            if 'locality' in component['types']:
                return component['long_name']
            elif 'administrative_area_level_2' in component['types']:
                return component['long_name']
    
    return "Did not find a city"



"""address = "Bohdalecká 1576, 101 00 Praha 10-Michle, Чехия"
city = get_city_from_address(address)
print("Город:", city)"""
