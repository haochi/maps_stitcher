from geo import LatLng, LatLngBounds
from TileMachine import TileMachine
from TileDownloader import TileDownloader
from TileStitcher import TileStitcher

from distutils.dir_util import mkpath
import argparse
import json
import os.path as path
import os

TILES_FILE_NAME = 'tiles.json'

def download(project):
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', action='store', required=True, help='Google API key')
    args, unknown = parser.parse_known_args()

    project_path = path.join(os.getcwd(), project)
    tiles_path = path.join(project_path, 'tiles')
    mkpath(tiles_path)

    with open(path.join(project_path, TILES_FILE_NAME)) as tiles_json:
        downloader = TileDownloader(tiles_path, json.load(tiles_json))
        downloader.download()

def init(project):
    parser = argparse.ArgumentParser()
    parser.add_argument('--zoom', action='store', type=int, default=1, help='Zoom level between 0 (world) to 21+ (street).')
    parser.add_argument('--scale', action='store', type=int, default=1, help='Scale of image (1, 2, 4)')
    parser.add_argument('--size', action='store', type=int, default=640, help='Size of image')
    parser.add_argument('--southwest', action='store', required=True, help='Southwest latitude and longitude. e.g. --southwest=39.1,-83.2')
    parser.add_argument('--northeast', action='store', required=True, help='Northeast latitude and longitude, e.g. --northeast=40.3,-82.4')
    args, unknown = parser.parse_known_args()

    project_path = path.join(os.getcwd(), project)

    tile_machine = TileMachine(size=args.size, zoom=args.zoom, scale=args.scale)
    def tiles_to_json(tiles): return map(lambda tile: { 'url': tile.url, 'x': tile.x, 'y': tile.y }, tiles)
    def parse_latlng(latlng_str): return map(lambda a: float(a), latlng_str.split(',', 2))

    bounds = LatLngBounds(
        LatLng(*parse_latlng(args.southwest)),
        LatLng(*parse_latlng(args.northeast)))
    
    mkpath(project_path)
    tiles = tile_machine.tiles_from_bounds(bounds)
    tiles_file = open(path.join(project_path, TILES_FILE_NAME), 'w')

    ouput = {
        'config': {
            'zoom': args.zoom,
            'size': args.size,
            'scale': args.scale,
            'southwest': args.southwest,
            'northeast': args.northeast
        },
        'tiles': {
            'primary': tiles_to_json(tiles['primary']),
            'half': tiles_to_json(tiles['half'])
        }
    }

    json.dump(ouput, tiles_file)

def stitch(project):
    parser = argparse.ArgumentParser()
    parser.add_argument('--save', action='store', default='output.jpg', help='File name')
    parser.add_argument('--format', action='store', default='JPEG', help='File type')
    args, unknown = parser.parse_known_args()

    project_path = path.join(os.getcwd(), project)
    tiles_path = path.join(project_path, 'tiles')
    output_path = path.join(project_path, args.save)

    with open(path.join(project_path, TILES_FILE_NAME)) as tiles_json:
        stitcher = TileStitcher(tiles_path, json.load(tiles_json))
        image = stitcher.stitch()
        image.save(output_path, args.format)
    

def main(args):
    commands = dict(download=download, stitch=stitch, init=init)
    if args.command in commands:
        commands[args.command](args.project)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('command', action='store', help='Command to execute (init, download, stitch)')
    parser.add_argument('project', action='store', help='Directory to store this project in')
    args, unknown = parser.parse_known_args()

    main(args)
