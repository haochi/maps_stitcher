from geo import Point, LatLng, LatLngBounds, Projection
import urllib
import math

projection = Projection()

class Tile(object):
    def __init__(self, x, y, url):
        self.x = x
        self.y = y
        self.url = url

class TileMachine(object):
    def __init__(self, size, zoom, scale):
        self.size = size
        self.zoom = zoom 
        self.scale = scale
        self.zoom_scale = 1 << self.zoom

    def tiles_from_bounds(self, bounds):
        primary_tiles = []
        half_way_tiles = []
        max_x = 0

        params = dict(zoom=self.zoom, scale=self.scale, size='{0}x{0}'.format(self.size))

        # generate an (x, y) grid based on the given bounds
        # then use skip_check=True to add (y+1) row and (x+1) column
        y = 0
        while True:
            x = 0
            while True:
                if not self.add_tile(bounds, x, y, primary_tiles, half_way_tiles, params):
                    self.add_tile(bounds, x, y, None, half_way_tiles, params, skip_check=True)
                    max_x = x
                    break
                x += 1
            y += 1

            if not bounds.contains(self.get_latlng_from_tile_at(bounds, 0, y)):
                for x in range(max_x + 1):
                    self.add_tile(bounds, x, y, None, half_way_tiles, params, skip_check=True)
                break

        return dict(primary=primary_tiles, half=half_way_tiles)

    def add_tile(self, bounds, x, y, primary_tiles, half_way_tiles, params, skip_check=False):
        latlng = self.get_latlng_from_tile_at(bounds, x, y)
        half_way_latlng = self.get_latlng_half_tile_away(latlng)

        if bounds.contains(latlng) or skip_check:
            if primary_tiles is not None:
                primary_tiles.append(self.latlng_to_tile(latlng, x, y, params))
            half_way_tiles.append(self.latlng_to_tile(half_way_latlng, x, y, params))
            return True

        return False

            
    def latlng_to_tile(self, latlng, x, y, params):
        url = self.generate_google_static_map_url_from_latlng(latlng, **params)
        return Tile(x, y, url)

    def get_latlng_from_tile_at(self, bounds, x, y):
        scale = self.size / float(self.zoom_scale)
        ne = bounds.getNorthEast()
        sw = bounds.getSouthWest()
        top_right = projection.fromLatLngToPoint(ne)
        bottom_left = projection.fromLatLngToPoint(sw)
        point = Point(float(x) * scale + bottom_left.x, float(y) * scale + top_right.y)
        
        return projection.fromPointToLatLng(point)

    def get_latlng_half_tile_away(self, latlng):
        center = projection.fromLatLngToPoint(latlng)
        half = -self.size / 2.0 / self.zoom_scale
        half_title_away = Point(half + center.x, half + center.y)
        return projection.fromPointToLatLng(half_title_away)


    def generate_google_static_map_url_from_latlng(self, latlng, **kwargs):
        base = 'https://maps.googleapis.com/maps/api/staticmap?'
        params = dict(center='{0},{1}'.format(latlng.lat, latlng.lng))
        params.update(kwargs)
        return base + urllib.urlencode(params)

