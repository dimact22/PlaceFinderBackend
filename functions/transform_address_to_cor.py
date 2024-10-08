from geopy.geocoders import GoogleV3

geolocator = GoogleV3(api_key="...")


def transform(address):
    try:
        location = geolocator.geocode(address)
        if location:
            return [location.latitude, location.longitude]
        else:
            print("///")
    except Exception as e:
        print(f"Error: {e}")
