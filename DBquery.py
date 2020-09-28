import netCDF4 as nc
import numpy as np
import math
from DBcreate import Lightning, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from netCDF4 import Dataset

engine = create_engine('sqlite:///sqlalchemy.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

# light = session.query(Lightning)\
#     .filter(Lightning.time == '20-08-01T04:00:00.000Z') \
#     .filter(Lightning.lat.between(41.001666266518185, 41.006146267))\
#     .filter(Lightning.lon.between(14.931793212890623, 14.937673213))\
#     .count()
#
# print(light)

# 41.001666266518185 14.931793212890623

# model = Dataset('/home/sli/Downloads/wrf5_d03_20200801Z0400.nc.nc4', "r+", format="NETCDF4")

# lat = model.dimensions['latitude'].size
# lon = model.dimensions['longitude'].size
# time = model.dimensions['time'].size

with nc.Dataset('/home/sli/Downloads/wrf5_d03_20200801Z1500.nc.nc4', format="NETCDF4") as src, nc.Dataset('/home/sli/Downloads/Test/test.nc.nc4', 'w', format="NETCDF4") as dst:
        # copy global attributes all at once via dictionary
    dst.setncatts(src.__dict__)
        # copy dimensions
    for name, dimension in src.dimensions.items():
        dst.createDimension(
            name, (len(dimension) if not dimension.isunlimited() else None))
    # copy all file data except for the excluded
    for name, variable in src.variables.items():
        # if name not in toexclude:
        x = dst.createVariable(name, variable.datatype, variable.dimensions)
        dst[name][:] = src[name][:]
        # copy variable attributes all at once via dictionary
        dst[name].setncatts(src[name].__dict__)

        # t = dst.createDimension("T", 1)
        # lt = dst.createDimension("X", 553)
        # ln = dst.createDimension("Y", 543)
        #
        # times = dst.createVariable("time", "f8", ("time",))
        # latitudes = dst.createVariable("lat", "f4", ("lat",))
        # longitudes = dst.createVariable("lon", "f4", ("lon",))
        #
        # lightCount = dst.createVariable("lightCount", "i4", ("time", "lat", "lon",))

model = Dataset('/home/sli/Downloads/Test/test.nc.nc4', "r+", format="NETCDF4")

model.createDimension('X', 553)
model.createDimension('Y', 543)
model.createDimension('t', 1)

lats = model.createVariable('lat', 'f4', ('X', 'Y'))
lats.units = 'degree_north'
lats._CoordinateAxisType = 'Lat'

lons = model.createVariable('lon', 'f4', ('X', 'Y'))
lons.units = 'degree_east'
lons._CoordinateAxisType = 'Lon'

lightCounter = model.createVariable('light', 'i4', ('t', 'latitude', 'longitude'))

deltaLat = (model['latitude'][1] - model['latitude'][0])
deltaLon = (model['longitude'][1] - model['longitude'][0])

# print(deltaLat)
# print(str(model['latitude'][552]) + ' ' + str(model['latitude'][0]))
# print(str(model['longitude'][542]) + ' ' + str(model['longitude'][0]))
# print(deltaLon)

lightMat = np.full([len(model['latitude']), len(model['longitude'])], 0, dtype=np.int)

for j in range(0, 553):
    for i in range(0, 543):
        cLat = (model['latitude'][j])
        cLon = (model['longitude'][i])
        center = (cLat, cLon)

        minLon = center[1] - deltaLon / 2
        minLat = center[0] - deltaLat / 2
        maxLon = center[1] + deltaLon / 2
        maxLat = center[0] + deltaLat / 2

        minC = (minLat, minLon)
        maxC = (maxLat, maxLon)

        # light = session.query(Lightning) \ .filter(Lightning.time == '20-08-01T04:00:00.000Z') \
        #     .count()

        light = session.query(Lightning) \
            .filter(Lightning.time == '20-08-01T15:00:00.000Z') \
            .filter(Lightning.lat.between(minLat, maxLat)) \
            .filter(Lightning.lon.between(minLon, maxLon)) \
            .count()

        lightMat[j][i] = light

        print('min' + str(minC[0]) + ' ' + str(minC[1]))
        print('max' + str(maxC[0]) + ' ' + str(maxC[1]))
        print(light)
        #if light != 0: break
        del light

lightCounter[0, :, :] = lightMat

for i in range(len(lightMat[:, 0])):
    for j in range(len(lightMat[0, :])):
        if lightMat[i][j] != 0:
            print(str(i) + ' '+str(j))


model.close()
