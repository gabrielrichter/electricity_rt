# title: 2.clean_temperature_2020.py
# author: Gabriel Richter de Almeida (FGV EPGE)
# date: 2020-09-13

# import modules
import os
import geopandas as gpd
import netCDF4
import numpy as np
import pandas as pd

# set paths
root = r'C:\Users\gabri\Desktop\electricity_rt'
data = os.path.join(root, 'data')
temp = os.path.join(root, 'temp')

# define lists and dictionaries
state_lst = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO',
             'MA', 'MG', 'MS', 'MT', 'PA', 'PB', 'PE', 'PI', 'PR',
             'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']

state_dic = {i: [] for i in state_lst}

year_lst = [str(i) for i in range(2020, 2021)]

# Note: https://confluence.ecmwf.int/display/CUSF/ERA5+CDS+requests+which+return+a+mixture+of+ERA5+and+ERA5T+data says
# that "The ERA5 hourly and monthly data are made available with a 3 month delay. This means that after a month has
# passed, another month's worth of ERA5 data is written to the dataset. ERA5T (near real time) preliminary data are
# used to fill the gap between the end of the ERA5 data and 5 days before the present date. The oldest month of these
# is overwritten each month as new ERA5 data become available. (...) For requests which return a mixture of ERA5 and
# ERA5T data, instantaneous variables (e.g temperature) come from ERA5T (which has 'experiment version' of 5). (...)
# When these data are converted to netCDF a new dimension is created called expver containing 1 (ERA5) and 5 (ERA5T).
# Moreover, a single time coordinate is used which covers the entire requested period."

# In practice, suppose today is 7/19/2020 and we download a '.nc' file with data ranging from 01/01/2020 to 7/31/2020.
# As per the explanation above, the file will only contain data from 01/01/2020 to 7/13/2020. Moreover, the t2m
# variable will have an additional dimension, called 'expver'. Suppose istart and istop are, respectively, the indices
# associated to the timestamp objects '01/01/2020' and '7/13/2020'. Assume that iy and ix are, respectively, a vector
# of latitudes and longitudes. Then, when k=0, the expression t2m[istart:istop + 1, k, iy, ix] will return non-nan t2m
# data (ERA5) covering the period 01/01/2020 to 04/30/2020, and nan t2m data from 05/01/2020 to 7/13/2020. On the other
# hand, when k=1, it will return nan t2m data from 01/01/2020 to 04/30/2020, and non-nan t2m data (ERA5T) covering the
# period 05/01/2020 to 7/13/2020

# run loop
for i in year_lst:
    year_name = i
    print('Year = ' + year_name)

    for j in list(state_dic.keys()):
        state_name = j.lower()
        print('State = ' + state_name)

        df_dic = {0: [], 1: []}  # 0 and 1 for, respectively, ERA5 and ERA5T datasets

        # load shapefile and extract variables
        state_df = gpd.read_file(os.path.join(data, 'shapefiles', f'{state_name}_Municipios_2019.shp'))  # note that
        # print(state_df.crs) returns "epsg:4674" - https://spatialreference.org/ref/epsg/4674/. However, ERA5 dataset
        # projection is "epsg:4326" - https://spatialreference.org/ref/epsg/wgs-84/
        state_df = state_df.to_crs(epsg=4326)  # fix the issue above

        municipality_df = pd.DataFrame(
            data=state_df[['CD_MUN', 'NM_MUN', 'SIGLA_UF']])  # create dataset with municipality information
        municipality_df.columns = ['id_municipality', 'municipality', 'state']

        state_df['centroid'] = state_df['geometry'].centroid  # calculate the centroid of every municipality
        centroid_outside = ~(state_df['centroid'].within(
            state_df['geometry']))  # boolean vector: TRUE if centroid lies outside the municipality geometry
        if centroid_outside.any():
            state_df.loc[
                centroid_outside, 'centroid'] = state_df['geometry'].representative_point()  # replace centroid by
            # representative point (centrality point which lies inside geometry) if centroid_outside==TRUE

        # plot a graph to perform sanity check on manipulated centroids
        # state_bounds = state_df.boundary.plot(linewidth=0.25)
        # state_df['centroid'].plot(ax=state_bounds, marker='.', color='red', markersize=0.25)
        # plt.pyplot.savefig(os.path.join(temp, f'{state_name}_{year_name}.pdf'))

        state_df['centr_lon'] = state_df['centroid'].x
        state_df['centr_lat'] = state_df['centroid'].y

        # load netcdf file and extract variables
        ds = netCDF4.Dataset(os.path.join(data, 'temperature', f'temp_hour_{year_name}.nc'))

        lat = ds.variables['latitude'][:]
        lon = ds.variables['longitude'][:]

        time = ds.variables['time']
        dtime = netCDF4.num2date(time[:], time.units, calendar=time.calendar,
                                 only_use_cftime_datetimes=False,
                                 only_use_python_datetimes=True)  # correction, since time is measured in hours since
        # 1900-01-01 00:00. Moreover, cftime object is also being converted to datetime object to allow for date/time
        # operations.

        # find the most representative temperature for each municipality
        def near(array, value):
            idx = (abs(array - value)).argmin()
            return idx

        ix = [near(lon, x) for x in state_df['centr_lon']]  # find the index of the closest point on the
        # temperature grid to each municipality's centroid longitude
        iy = [near(lat, x) for x in state_df['centr_lat']]

        start = pd.to_datetime(f'{year_name}-01-01 00:00')
        stop = pd.to_datetime(f'{year_name}-08-31 23:00')

        istart = netCDF4.date2index(start, time, calendar=time.calendar,
                                    select='exact')  # return time variable index corresponding to first day and hour
        # of the year
        istop = netCDF4.date2index(stop, time, calendar=time.calendar, select='exact')

        dtime = dtime[istart:istop + 1]  # set time index interval we want to retrieve data from

        for k in [0, 1]:  # 0 and 1 for, respectively, ERA5 and ERA5T datasets
            t2m = ds.variables['t2m'][:] - 273.15  # converts from kelvin to celsius
            t2m[t2m == -32767 - 273.15] = np.nan  # converts nan sentinel (= -32767) to nan

            t2m = t2m[istart:istop + 1, k, iy, ix]  # find temperature associated with each element of
            # (time=istart:istop, k={0 if expver=1; 1, if expver=5}, lat=iy, lon=ix) quadruple

            df = pd.DataFrame(data=t2m, index=dtime,
                              columns=[state_df['NM_MUN'].values])  # create dataset with desirable information
            df = df.unstack().reset_index()
            df.columns = ['municipality', 'date', 'temperature']

            df = df[df['temperature'].notna()]

            df_dic[k] = df

        df = pd.concat(df_dic.values())  # concatenate ERA5 and ERA5T datasets

        df = df.sort_values(['municipality', 'date'], ascending=True)

        # add 'id_municipality' and 'state' variables
        df = df.merge(right=municipality_df,
                      how='left',
                      on='municipality',
                      validate='m:1'
                      )

        df = df.set_index('date')

        state_dic[j] = df

    df = pd.concat(state_dic.values())  # append datasets

    df['temperature'] = df['temperature'].astype('float32')  # optimize memory usage
    df[['municipality', 'id_municipality', 'state']] = df[['municipality', 'id_municipality', 'state']].astype(
        'category')  # optimize memory usage

    df = df[['state', 'municipality', 'id_municipality', 'temperature']]  # reorder columns

    df.to_pickle(os.path.join(temp, f'temperature_{year_name}.pkl'))  # save dataset in pickle (serialized) format
