from geo import Point, LatLng, LatLngBounds, Projection
import urllib
import math

MAX_SIZE = 9999

projection = Projection()

class Tile(object):
    def __init__(self, x, y, url):
        self.x = x
        self.y = y
        self.url = url

    def __str__(self):
        return self.url

class TileMachine(object):
    def __init__(self, size, zoom, scale, format, maptype, params):
        self.size = size
        self.zoom = zoom 
        self.scale = scale
        self.zoom_scale = 1 << self.zoom
        self.format = format
        self.maptype = maptype
        self.extra_params = filter(lambda param: '=' in param, params)

    def tiles_from_bounds(self, bounds):
        primary_tiles = []
        half_way_tiles = []
        max_x = max_y = 0

        params = dict(zoom=self.zoom, scale=self.scale, size='{0}x{0}'.format(self.size),
                      format=self.format, maptype=self.maptype)

        """ generate an (x, y) grid based on the given bounds
            [*][*][*]
            [*][*][*]
        """
        for y in range(MAX_SIZE):
            for x in range(MAX_SIZE):
                if not self.add_tile(bounds, x, y, primary_tiles, half_way_tiles, params):
                    max_x = max(max_x, x)
                    break
            if not bounds.contains(self.get_latlng_from_tile_at(bounds, 0, y)):
                max_y = max(max_y, y)
                break

        """ then use skip_check=True to add (y+1) row and (x+1) column
            [*][*][*][ ]
            [*][*][*][ ]
            [ ][ ][ ][ ]
        """
        for y in range(max_y):
            self.add_tile(bounds, max_x, y, None, half_way_tiles, params, skip_check=True)

        for x in range(max_x):
            self.add_tile(bounds, x, max_y, None, half_way_tiles, params, skip_check=True)

        self.add_tile(bounds, max_x, max_y, None, half_way_tiles, params, skip_check=True)

        return dict(primary=primary_tiles, half=half_way_tiles)

    def add_tile(self, bounds, x, y, primary_tiles, half_way_tiles, params, skip_check=False):
        latlng = self.get_latlng_from_tile_at(bounds, x, y)
        half_way_latlng = self.get_latlng_half_tile_away(latlng)

        if LatLng.valid_latlng(latlng) and (bounds.contains(latlng) or skip_check):
            if primary_tiles is not None:
                primary_tiles.append(self.latlng_to_tile(latlng, x, y, params))

            if LatLng.valid_latlng(half_way_latlng) and (bounds.contains(half_way_latlng) or skip_check):
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
        return '{0}{1}&{2}'.format(base, urllib.urlencode(params), '&'.join(self.extra_params))
