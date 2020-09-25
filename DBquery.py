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

# with nc.Dataset('/home/sli/Downloads/Test/wrf5_d03_20200801Z0400.nc.nc4', format="NETCDF4") as src, nc.Dataset('/home/sli/Downloads/Test/test.nc.nc4', 'w', format="NETCDF4") as dst:
#         # copy global attributes all at once via dictionary
#     dst.setncatts(src.__dict__)
#         # copy dimensions
#     for name, dimension in src.dimensions.items():
#         dst.createDimension(
#             name, (len(dimension) if not dimension.isunlimited() else None))
#     # copy all file data except for the excluded
#     for name, variable in src.variables.items():
#         # if name not in toexclude:
#         x = dst.createVariable(name, variable.datatype, variable.dimensions)
#         dst[name][:] = src[name][:]
#         # copy variable attributes all at once via dictionary
#         dst[name].setncatts(src[name].__dict__)
#
#         # t = dst.createDimension("T", 1)
#         # lt = dst.createDimension("X", 553)
#         # ln = dst.createDimension("Y", 543)
#         #
#         # times = dst.createVariable("time", "f8", ("time",))
#         # latitudes = dst.createVariable("lat", "f4", ("lat",))
#         # longitudes = dst.createVariable("lon", "f4", ("lon",))
#         #
#         # lightCount = dst.createVariable("lightCount", "i4", ("time", "lat", "lon",))

model = Dataset('/home/sli/Downloads/Test/wrf5_d03_20200801Z0400.nc.nc4', "r+", format="NETCDF4")

model.createDimension('X',553)
model.createDimension('Y', 543)
model.createDimension('t',1)

lats = model.createVariable('lat', 'f4', ('X', 'Y'))
lats.units = 'degree_north'
lats._CoordinateAxisType = 'Lat'

lons = model.createVariable('lon', 'f4', ('X', 'Y'))
lons.units = 'degree_east'
lons._CoordinateAxisType = 'Lon'

lightCounter = model.createVariable('light', 'i4', ('t', 'latitude', 'longitude'))


# print (lat)
# lightCount = model.createVariable('lightCount', 'i4', 'time', 'lat', 'lon')

# model.createDimension('latitude', len(model['latitude']))
# model.createDimension('longitude', len(model['longitude']))
# model.createDimension('time', 1)


#
# MODEL_CLDFRA_TOTAL = model['CLDFRA_TOTAL'][::]
# MODEL_DAILY_RAIN = model['DAILY_RAIN'][::]
# MODEL_DELTA_RAIN = model['DELTA_RAIN'][::]
# MODEL_DELTA_WDIR10 = model['DELTA_WDIR10'][::]
# MODEL_DELTA_WSPD10 = model['DELTA_WSPD10'][::]
# MODEL_GPH500 = model['GPH500'][::]
# MODEL_GPH850 = model['GPH850'][::]
# MODEL_HOURLY_SWE = model['HOURLY_SWE'][::]
# MODEL_MCAPE = model['MCAPE'][::]
# MODEL_RH2 = model['RH2'][::]
# MODEL_RH300 = model['RH300'][::]
# MODEL_RH500 = model['RH500'][::]
# MODEL_RH700 = model['RH700'][::]
# MODEL_RH850 = model['RH850'][::]
# MODEL_RH950 = model['RH950'][::]
# MODEL_SLP = model['SLP'][::]
# MODEL_T2C = model['T2C'][::]
# MODEL_TC500 = model['TC500'][::]
# MODEL_TC850 = model['TC850'][::]
# MODEL_U10M = model['U10M'][::]
# MODEL_U300 = model['U300'][::]
# MODEL_U500 = model['U500'][::]
# MODEL_U700 = model['U700'][::]
# MODEL_U850 = model['U850'][::]
# MODEL_U950 = model['U950'][::]
# MODEL_WDIR10 = model['WDIR10'][::]
# MODEL_WSPD10 = model['WSPD10'][::]

# lightNum = np.full([len(model['latitude']), len(model['longitude'])], 0, dtype=np.float32)
# Dataset.createVariable()

deltaLat = (model['latitude'][1] - model['latitude'][0])
deltaLon = (model['longitude'][1] - model['longitude'][0])

# print(deltaLat)
# print(str(model['latitude'][552]) + ' ' + str(model['latitude'][0]))
# print(str(model['longitude'][542]) + ' ' + str(model['longitude'][0]))
# print(deltaLon)

# light = session.query(Lightning)\
#     .filter(Lightning.time == '20-08-01T04:00:00.000Z') \
#     .filter(Lightning.lat.between(41.001666266518185, 41,006146267))\    41.001666266518185 14.931793212890623
#     .filter(Lightning.lon.between(14.931793212890623, 16.3))\
#     .count()

# print(light)
#
#
lightMat = np.full([len(model['latitude']), len(model['longitude'])], 0, dtype=np.int)
#
for j in range(0, 552):
    for i in range(0, 542):
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

lightCounter[0,:,:]=lightMat

for i in range(len(lightMat[:,0])):
    for j in range (len(lightMat[0,:])):
        if lightMat[i][j] !=0:
            print(str(i)+ ' '+str(j))
#
# aggregated_file = nc.Dataset('TEST.nc', 'w', format='NETCDF4')
#
# aggregated_file.createDimension('X', len(model['latitude']))
# aggregated_file.createDimension('Y', len(model['longitude']))
#
# lats = aggregated_file.createVariable('lat', 'f4', ('X', 'Y'))
# lats.units = 'degree_north'
# lats._CoordinateAxisType = 'Lat'
#
# lons = aggregated_file.createVariable('lon', 'f4', ('X', 'Y'))
# lons.units = 'degree_east'
# lons._CoordinateAxisType = 'Lon'
#
# CLDFRA_TOTAL = aggregated_file.createVariable('HGT', 'f4', ('X', 'Y'), fill_value=-999)
# DAILY_RAIN = aggregated_file.createVariable('DAILY_RAIN', 'f4', ('X', 'Y'), fill_value=-999)
# DELTA_RAIN = aggregated_file.createVariable('DELTA_RAIN', 'f4', ('X', 'Y'), fill_value=-999)
# DELTA_WDIR10 = aggregated_file.createVariable('DELTA_WDIR10', 'f4', ('X', 'Y'), fill_value=-999)
# DELTA_WSPD10 = aggregated_file.createVariable('DELTA_WSPD10', 'f4', ('X', 'Y'), fill_value=-999)
# GPH500 = aggregated_file.createVariable('GPH500', 'f4', ('X', 'Y'), fill_value=-999)
# GPH850 = aggregated_file.createVariable('GPH850', 'f4', ('X', 'Y'), fill_value=-999)
# HOURLY_SWE = aggregated_file.createVariable('HOURLY_SWE', 'f4', ('X', 'Y'), fill_value=-999)
# MCAPE = aggregated_file.createVariable('MCAPE', 'f4', ('X', 'Y'), fill_value=-999)
# RH2 = aggregated_file.createVariable('RH2', 'f4', ('X', 'Y'), fill_value=-999)
# RH300 = aggregated_file.createVariable('RH300', 'f4', ('X', 'Y'), fill_value=-999)
# RH500 = aggregated_file.createVariable('RH500', 'f4', ('X', 'Y'), fill_value=-999)
# RH700 = aggregated_file.createVariable('RH700', 'f4', ('X', 'Y'), fill_value=-999)
# RH850 = aggregated_file.createVariable('RH850', 'f4', ('X', 'Y'), fill_value=-999)
# RH950 = aggregated_file.createVariable('RH950', 'f4', ('X', 'Y'), fill_value=-999)
# SLP = aggregated_file.createVariable('SLP', 'f4', ('X', 'Y'), fill_value=-999)
# T2C = aggregated_file.createVariable('T2C', 'f4', ('X', 'Y'), fill_value=-999)
# TC500 = aggregated_file.createVariable('TC500', 'f4', ('X', 'Y'), fill_value=-999)
# TC850 = aggregated_file.createVariable('TC850', 'f4', ('X', 'Y'), fill_value=-999)
# U10M = aggregated_file.createVariable('U10M', 'f4', ('X', 'Y'), fill_value=-999)
# U300 = aggregated_file.createVariable('U300', 'f4', ('X', 'Y'), fill_value=-999)
# U500 = aggregated_file.createVariable('U500', 'f4', ('X', 'Y'), fill_value=-999)
# U700 = aggregated_file.createVariable('U700', 'f4', ('X', 'Y'), fill_value=-999)
# U850 = aggregated_file.createVariable('U850', 'f4', ('X', 'Y'), fill_value=-999)
# U950 = aggregated_file.createVariable('U950', 'f4', ('X', 'Y'), fill_value=-999)
# WDIR10 = aggregated_file.createVariable('WDIR10', 'f4', ('X', 'Y'), fill_value=-999)
# WSPD10 = aggregated_file.createVariable('WSPD10', 'f4', ('X', 'Y'), fill_value=-999)
# LIGHTNUM = aggregated_file.createVariable('LIGHTNUM', 'f4', ('X', 'Y'), fill_value=-999)
#
#
# CLDFRA_TOTAL[::] = MODEL_CLDFRA_TOTAL
# DAILY_RAIN[::] = MODEL_DAILY_RAIN
# DELTA_RAIN[::] = MODEL_DELTA_RAIN
# DELTA_WDIR10[::] = MODEL_DELTA_WDIR10
# DELTA_WSPD10[::] = MODEL_DELTA_WSPD10
# GPH500[::] = MODEL_GPH500
# GPH850[::] = MODEL_GPH850
# HOURLY_SWE[::] = MODEL_HOURLY_SWE
# MCAPE[::] = MODEL_MCAPE
# RH2[::] = MODEL_RH2
# RH300[::] = MODEL_RH300
# RH500[::] = MODEL_RH500
# RH700[::] = MODEL_RH700
# RH850[::] = MODEL_RH850
# RH950[::] = MODEL_RH950
# T2C[::] = MODEL_T2C
# TC500[::] = MODEL_TC500
# TC850[::] = MODEL_TC850
# U10M[::] = MODEL_U10M
# U300[::] = MODEL_U300
# U500[::] = MODEL_U500
# U700[::] = MODEL_U700
# U850[::] = MODEL_U850
# U950[::] = MODEL_U950
# WDIR10[::] = MODEL_WDIR10
# WSPD10[::] = MODEL_WSPD10
# LIGHTNUM[::] = lightMat[::]


model.close()
