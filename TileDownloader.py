import grequests
import json
import os
import os.path as path

class TileDownloader(object):
    def __init__(self, tiles_path, tiles_json, key, skip):
        tiles = tiles_json['tiles']
        self.tiles_path = tiles_path
        self.key = key

        self.config = tiles_json['config']
        self.primary = tiles['primary']
        self.half = tiles['half']
        self.skip = skip

    def download(self):
        self.download_tiles(self.primary)
        self.download_tiles(self.half, prefix='half-')
        
    def download_tiles(self, tiles, prefix=''):
        batches = chunks(tiles, 10)
        for batch in batches:
            self.download_batch(batch, prefix)

    def download_batch(self, batch, prefix):
        if self.skip:
            batch = filter(lambda tile: not os.path.isfile(tile_path(self.tiles_path, prefix, tile['x'], tile['y'])), batch)
            print('batch_size', len(batch))

        rs = (grequests.get('{0}&key={1}'.format(tile['url'], self.key)) for tile in batch)
        responses = grequests.map(rs)

        for index in range(len(batch)):
            response = responses[index]
            tile = batch[index]
            if response.status_code == 200:
                file_name = tile_path(self.tiles_path, prefix, tile['x'], tile['y'])
                save_response_to(response, file_name)
            else:
                print(response.status_code)

def tile_path(directory, prefix, x, y):
    return path.join(directory, '{prefix:s}{x:d}x{y:d}'.format(prefix=prefix, x=x, y=y))
    
def save_response_to(response, path):
    with open(path, 'wb') as f:
        for chunk in response.iter_content():
            f.write(chunk)
        
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]
    
