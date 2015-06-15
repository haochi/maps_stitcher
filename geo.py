import math

EPSILON = 1e-10

class LatLngBounds(object):
    def __init__(self, south_west, north_east):
        self.south_west = LatLng(south_west.lat, south_west.lng)
        self.north_east = LatLng(north_east.lat, north_east.lng)

    def contains(self, latlng):
        ne = self.north_east
        sw = self.south_west
        sw2 = ne2 = latlng

        return gte(sw2.lat, sw.lat) and lte(ne2.lat, ne.lat) and\
               gte(sw2.lng, sw.lng) and lte(ne2.lng, ne.lng)

    def getSouthWest(self):
        return LatLng(self.south_west.lat, self.south_west.lng)

    def getNorthEast(self):
        return LatLng(self.north_east.lat, self.north_east.lng)

    def __str__(self):
        return '\t\t{0}\n{1}'.format(self.north_east, self.south_west)

class LatLng(object):
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def __str__(self):
        return 'LatLng({0}, {1})'.format(self.lat, self.lng)

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Projection(object):
    PIXELS = float(256)
    DEGREES_IN_CIRCLE = float(360)
    PIXELS_PER_DEGREE = PIXELS / DEGREES_IN_CIRCLE
    MID_POINT= Point(PIXELS / 2, PIXELS / 2)

    def fromLatLngToPoint(self, latlng):
        point = Point(0, 0)

        point.x = self.MID_POINT.x + latlng.lng * self.PIXELS_PER_DEGREE
        e = min(math.sin(math.radians(latlng.lat)), 1 - 1e-15)
        point.y = self.MID_POINT.y + 0.5 * math.log((1 + e) / (1 - e)) * -self.PIXELS / (2 * math.pi)
        return point
        
    def fromPointToLatLng(self, point):
        lat = ( 2 * math.atan(math.exp((point.y - self.MID_POINT.y) / - ( self.PIXELS / (2 * math.pi)))) - math.pi / 2) /(math.pi/(self.DEGREES_IN_CIRCLE/2))
        lng = (point.x - self.MID_POINT.x) / self.PIXELS_PER_DEGREE
        return LatLng(lat, lng)

def gte(a, b):
    return a > b or abs(a - b) <= EPSILON

def lte(a, b):
    return b > a or abs(a - b) <= EPSILON

if __name__ == '__main__':
    p = Projection()
    point = p.fromLatLngToPoint(LatLng(1,1))
    print(point.x, point.y)
    latlng = p.fromPointToLatLng(Point(1,1))
    print(latlng.lat, latlng.lng)
