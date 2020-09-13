# title: 1.import_temperature.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# This file:
# 1) Requests API information from https://cds.climate.copernicus.eu/
#   1.1) Follow the instructions at https://confluence.ecmwf.int/display/CKB/How+to+install+and+use+CDS+API+on+Windows
# 2) Downloads:
#   2.1) ERA5 'reanalysis-era5-single-levels' dataset
#   2.2) Product: Athmosferic reanalysis of the global climate, w/ 0.25°x0.25° grid resolution by default
#   2.3) Variable: temperature (in Kelvin) of the air at 2m above the surface of land, sea or in-land waters
#   2.3) Years: 2000 to 2020, downloaded separately
#   2.4) Months: January to December
#   2.5) Days: 01 to 31
#   2.6) Hours/Time: 00:00 to 23:00
#   2.7) Area: 6N, -74W, -34S, -34E = Brazil bounding box
# 3) Saves file 'temp_hour_year.nc' at C:\Users\gabri\Google Drive\Gabriel\Educacao\Eletricidade-RT\data\nc


import os
import cdsapi

root = r'C:\Users\gabri\Desktop\electricity_rt'
data = os.path.join(root, 'data')

for year in range(2001, 2020):  # if current date is eg. September/2020, use range(2020, 2021)
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': ['2m_temperature'],
            'year': year,
            'month': [str(x).zfill(2) for x in range(1, 13)],
            'day': [str(x).zfill(2) for x in range(1, 32)],
            'area': [6, -74, -34, -34],  # N/W/S/E
            'time': [str(x).zfill(2) + r':00' for x in range(0, 24)]
        },
        os.path.join(data, 'temperature', f'temp_hour_{year}.nc')
    )
