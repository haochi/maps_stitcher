Maps Stitcher
=============

Downloads and generates an image of a map given a latitude and longitude bounds.

You can find some [sample output on Flickr here](https://www.flickr.com/photos/haochi/sets/72157653869432590). 

Environment
-----------

Running this script requires Python, plus some libraries.
You can see the dependencies in the `requirements.txt` file.

It's test with Python 2.7.6 inside [virtualenv](https://pypi.python.org/pypi/virtualenv)

Usage
-----

There are three steps to generate the image:

* Initialize the project with the latitude and longitude bounds (plus some other configurations)
* Download the necessary tiles with your [Google API key](https://developers.google.com/maps/documentation/javascript/tutorial#api_key)
* Stitch the tiles into the final image

The corresponding commands are (example):

* `maps_stitcher.py init PROJECT_NAME`: This will create a folder by the given project name in the current working directory.
    * `--southwest`: (**required**, comma separated latitude and longitude pair) south west bound
    * `--northeast`: (**required**, comma separated latitude and longitude pair) north east bound
    * `--zoom`: (optional, integer, default=1) [zoom level](https://developers.google.com/maps/documentation/staticmaps/#Zoomlevels), [1, 21+]
    * `--scale`: (optional, integer, default=1) [scale](https://developers.google.com/maps/documentation/staticmaps/#scale_values), (1, 2, 4)
    * `--size`: (option, integer, default=640) [size](https://developers.google.com/maps/documentation/staticmaps/#Imagesizes), [1, 2048]
    * `--format`: (optional, string, default=gif) Image format ([supported formats](https://developers.google.com/maps/documentation/static-maps/intro#ImageFormats))
    * `--maptype`: (optional, string, default=roadmap) Map type ([supported formats](https://developers.google.com/maps/documentation/static-maps/intro#MapTypes))


* `maps_stitcher.py download PROJECT_NAME`: This will start downloading the tiles
    * `--key`: (**required**, string) [Google API key](https://developers.google.com/maps/documentation/javascript/tutorial#api_key)

* `maps_stitcher.py stitch PROJECT_NAME`: This will stitch the tiles and generate the map
    * `--save`: (optional, string, default=output.gif) File name
    * `--format`: (optional, string, default=gif) File format ([supported formats](http://pillow.readthedocs.org/en/latest/handbook/image-file-formats.html))

#### Example

* `./maps_stitcher.py init san_francisco --southwest=37.708894,-122.502316 --northeast=37.808034,-122.358378 --zoom=15 --scale=2`
* `./maps_stitcher.py download san_francisco --key=ABCDEFG`
* `./maps_stitcher.py stitch san_francisco --output=sf.jpg`
