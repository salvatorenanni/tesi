import math
import os.path

import cv2
import numpy as np
import requests

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from DBcreate import Base, Lightning

engine = create_engine('sqlite:///sqlalchemy.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


save_path = '/home/sli/tiles'
coordinates = os.path.join(save_path, "coordinates.txt")
z = 10


def circlePrinter(newImg):
    # Draw the circumference of the circle.
    cv2.circle(newImg, (a, b), r, (0, 255, 0), 2)

    # Draw a small circle (of radius 1) to show the center.
    cv2.circle(newImg, (a, b), 1, (0, 0, 255), 3)
    cv2.imshow("Detected Circle" + item, newImg)
    cv2.waitKey(0)


def resizer(resImage):
    scale_percent = 220  # percent of original size  back to 256 *45.5/100
    width = int(resImage.shape[1] * scale_percent / 100)
    height = int(resImage.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(resImage, dim, interpolation=cv2.INTER_AREA)
    return resized


def getTile(cx, cy, cz):
    for i in range(0, 23):
        if i < 10:
            string = '2020-08-01T0' + str(i) + ':00:00.000Z'
            if i < 9:
                string1 = '2020-08-01T0' + str(i + 1) + ':00:00.000Z'
            else:
                string1 = '2020-08-01T' + str(i + 1) + ':00:00.000Z'
        else:
            string = '2020-08-01T' + str(i) + ':00:00.000Z'
            string1 = '2020-08-01T' + str(i + 1) + ':00:00.000Z'

        query = {'x': cx, 'y': cy, 'z': cz, 's': '256', 'from': string,
                 'to': string1}
        req = requests.get("https://tiles.lightningmaps.org/?", params=query)

        fileName = os.path.join(save_path, 'x' + str(x) + 'y' + str(y) + string + ".png")
        image = open(fileName, "wb")
        image.write(req.content)
        image.close()


class GlobalMercator(object):

    def __init__(self, tileSize=256):
        self.tileSize = tileSize
        self.initialResolution = 2 * math.pi * 6378137 / self.tileSize
        self.originShift = 2 * math.pi * 6378137 / 2.0

    '''Initialize the TMS Global Mercator pyramid'''

    # 156543.03392804062 for tileSize 256 pixels
    # 20037508.342789244

    def MetersToLatLon(self, mx, my):
        """Converts XY point from Spherical Mercator EPSG:900913 to lat/lon in WGS84 Datum"""

        lon = (mx / self.originShift) * 180.0
        lat = (my / self.originShift) * 180.0

        lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
        return lat, lon

    def Resolution(self, zoom):
        """Resolution (meters/pixel) for given zoom level (measured at Equator)"""

        # return (2 * math.pi * 6378137) / (self.tileSize * 2**zoom)
        return self.initialResolution / (2 ** zoom)

    def PixelsToMeters(self, px, py, zoom):
        """Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"""

        res = self.Resolution(zoom)
        mx = px * res - self.originShift
        my = py * res - self.originShift
        return mx, my

    def TileBounds(self, tx, ty, zoom):
        """Returns bounds of the given tile in EPSG:900913 coordinates"""

        minx, miny = self.PixelsToMeters(tx * self.tileSize, ty * self.tileSize, zoom)
        maxx, maxy = self.PixelsToMeters((tx + 1) * self.tileSize, (ty + 1) * self.tileSize, zoom)
        return minx, miny, maxx, maxy

    def GoogleTile(self, tx, ty, zoom):
        """Converts TMS tile coordinates to Google Tile coordinates"""

        # coordinate origin is moved from bottom-left to top-left corner of the extent
        return tx, (2 ** zoom - 1) - ty


for x in range(549, 559):
    for y in range(381, 391):
        getTile(x, y, z)

for item in os.listdir(save_path):
    if item.endswith(".png"):
        img = cv2.imread(save_path + '/' + item, cv2.IMREAD_COLOR)
        resized = resizer(img)

        # test only
        # cv2.imshow("Resized image " + item, resized)
        # cv2.waitKey(0)
        # cv2.destroyWindow("Resized image " + item)

        gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)

        detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 5, param1=30, param2=15, minRadius=0,
                                            maxRadius=15)

        # Draw circles that are detected.
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                a = int(round((a * 45.5) / 100, 0))
                b = int(round((b * 45.5) / 100, 0))

                # test only
                #circlePrinter(img)

                print('a ' + str(a) + '\t' + 'b ' + str(b) + '\n')

                mercator = GlobalMercator()
                minx, miny, maxx, maxy = mercator.TileBounds(x, y, z)
                # print('minx ' + str(minx) + '\t' + 'y ' + str(miny) + '\t' + 'maxx ' + str(maxx) + '\t' + 'maxy ' +
                # str(maxy) + '\n')

                print('x ' + str(minx) + '\t' + 'y ' + str(miny) + '\n')
                print('lat' + 'long' + str(mercator.MetersToLatLon(minx, miny)))
                res = mercator.Resolution(z)
                lat = abs(miny + b * res)
                long = abs(minx + a * res)
                print('x ' + str(long) + '\t' + 'y' + str(lat) + '\n')
                # print ("resol" + str(res))
                lat, long = mercator.MetersToLatLon(long, lat)

                print('lat ' + str(lat) + '\t' + 'y ' + str(long) + '\n')

                if os.path.exists(coordinates):
                    append_write = 'a'
                else:
                    append_write = 'w'

                newString = item[-26:]
                newString = newString[:-4]

                new_lightning = Lightning(lat=lat, lon=long, time=newString)

                session.add(new_lightning)
                session.commit()

                file = open(coordinates, append_write)
                file.write(str(lat) + " " + str(long) + " " + newString + "\n")
                file.close()
                del mercator
                # cv2.destroyWindow("Detected Circle"+item)

        os.remove(save_path + '/' + item)