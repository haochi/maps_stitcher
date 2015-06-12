from PIL import Image
import os.path as path

class TileStitcher(object):
    def __init__(self, tiles_path, tiles_json):
        tiles = tiles_json['tiles']

        self.tiles_path = tiles_path
        self.config = tiles_json['config']
        self.primary = tiles['primary']
        self.half = tiles['half']

        last_tile = self.primary[-1]
        self.size = self.config['size'] * self.config['scale']
        self.crop = (0, 0, self.size, self.size - 30 * self.config['scale'])
        self.x_tiles = last_tile['x'] + 1
        self.y_tiles = last_tile['y'] + 1

    def stitch(self):
        im = Image.new('RGB', (self.size * self.x_tiles, self.size * self.y_tiles))
        self.combine_tiles(im, self.primary)
        self.combine_tiles(im, self.half, prefix='half-', offset=-self.size/2, crop=True)

        return im

    def combine_tiles(self, image, tiles, prefix='', offset=0, crop=False):
        for tile in tiles:
            x, y = tile['x'], tile['y']
            tile_image_path = path.join(self.tiles_path, '{prefix:s}{x:d}x{y:d}'.format(x=x, y=y, prefix=prefix))
            img = Image.open(tile_image_path)
            if crop:
                img = img.crop(self.crop)

            image.paste(img, (x * self.size + offset, y * self.size + offset))
