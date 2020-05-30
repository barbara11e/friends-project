import googlemaps
from googlemaps.exceptions import HTTPError
from app import app

class Geolocator:
    def __init__(self, address: str):
        self.address = address


    def get_coords(self) -> dict:
        gmaps = googlemaps.Client(key=app.config['GOOGLE_MAPS_KEY'])
        try:
            geocode_result = gmaps.geocode(self.address)
            if geocode_result:
                lat = geocode_result[0]['geometry']['location']['lat']
                lng = geocode_result[0]['geometry']['location']['lng']
                return {'lat': lat, 'lng': lng}
            return {}
        except HTTPError:
            return {}
        else:
            return {}

    def str_coords(self) -> str:
        '''
        return: joined user location coordinates(lat, long) into string
        '''
        h = self.get_coords()
        s = ';'.join([str(_) for _ in h.values()])
        return s