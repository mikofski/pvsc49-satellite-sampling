import calendar
import pathlib
import matplotlib as mpl
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import pvlib
import rdtools
import seaborn as sns

sns.set(font_scale=1.5, rc={'figure.figsize': (16, 10)})
mpl.rcParams['figure.figsize'] = (16, 10)

DAYMINUTES = 24*60
KELVINS = 273.15
MAX_GHI_RATIO = 1.5

def get_irrad_components(ghi, zenith, TIMES):
    # get irrad components
    irrad = pvlib.irradiance.erbs(ghi, zenith, TIMES)
    dni = irrad.dni.values
    dhi = irrad.dhi.values
    kt = irrad.kt.values  # clearness index
    # calculate irradiance inputs
    dni_extra = pvlib.irradiance.get_extra_radiation(TIMES).values
    return irrad, dni, dhi, kt, dni_extra


def poop(weather_year, TIMES, LATITUDE, LONGITUDE, solar_zenith, ELEVATION,
         dni_extra, df, ):
    # estimate air temp
    year_start = weather_year.parts[-1]
    TL = pvlib.clearsky.lookup_linke_turbidity(TIMES, LATITUDE, LONGITUDE)
    AM = pvlib.atmosphere.get_relative_airmass(solar_zenith)
    PRESS = pvlib.atmosphere.alt2pres(ELEVATION)
    AMA = pvlib.atmosphere.get_absolute_airmass(AM, PRESS)
    CS = pvlib.clearsky.ineichen(solar_zenith, AMA, TL, ELEVATION, dni_extra)

    # estimate air temp
    est_air_temp, temp_adj, ghi_ratio, daily_delta_temp, cs_temp_air = \
        estimate_air_temp(year_start, df, LATITUDE, LONGITUDE, CS)
    temp_air = est_air_temp['Adjusted Temp (C)'].loc[TIMES].values
    ghi_ratio.describe()
    est_air_temp.head()

    f, ax = plt.subplots(2, 1, sharex=True, figsize=(16, 10))
    df.temp_air.plot(ax=ax[0], label='SURFRAD')
    est_air_temp[['Clear Sky Temperature (C)', 'Adjusted Temp (C)']].plot(ax=ax[0])
    ax[0].legend()
    CS.ghi.plot(ax=ax[1], label='CS')
    df.ghi.plot(ax=ax[1])
    ax[1].legend()
    plt.tight_layout()


def estimate_air_temp(year_start, surfrad, lat, lon, cs, max_ghi_ratio=MAX_GHI_RATIO):
    """
    Use clear sky temps scaled by daily ratio of measured to clear sky global
    insolation.

    Parameters
    ----------
    year_start : str
        SURFRAD data year
    surfrad : pandas.DateFrame
        surfrad data frame
    lat : float
        latitude in degrees north of equator [deg]
    lon : float
        longitude in degrees east of prime meridian [deg]
    cs : pandas.DataFrame
        clear sky irradiances [W/m^2]
    max_ghi_ratio : float
        daily GHI to clear sky GHI ratio is clipped at this limit

    Returns
    -------
    est_air_temp : pandas.DataFrame
        estimated air temperature in Celsius [C]
    temp_adj : pandas.Series
        temperature adjustment [C}
    ghi_ratio : pandas.Series
        ratio of  daily SURFRAD to clearsky GHI insolation
    daily_delta_temp : numpy.array
        daily temperature range, max - min, in Kelvin [K]
    cs_temp_air : pandas.Series
        clear sky air temperatures in Celsius [C]

    """
    daze = 367 if calendar.isleap(int(year_start)) else 366
    # create a leap year of minutes for the given year at UTC
    year_minutes = pd.date_range(
        start=year_start, freq='T', periods=daze*DAYMINUTES, tz='UTC')
    # clear sky temperature
    cs_temp_air = rdtools.clearsky_temperature.get_clearsky_tamb(
        year_minutes, lat, lon)
    # organize by day
    cs_temp_daily = cs_temp_air.values.reshape((daze, DAYMINUTES)) + KELVINS
    # get daily temperature range
    daily_delta_temp = np.array([td.max()-td.min() for td in cs_temp_daily])
    daily_delta_temp = pd.Series(
        daily_delta_temp, index=cs_temp_air.resample('D').mean().index)
    # calculate ratio of daily insolation versus clearsky
    ghi_ratio = surfrad.ghi.resample('D').sum() / cs.ghi.resample('D').sum()
    # limit ghi ratio and remove +/-inf
    ghi_ratio = np.clip(ghi_ratio, 0, max_ghi_ratio)
    ghi_ratio = ghi_ratio.rename('ghi_ratio')
    # apply ghi ratio to next day, wrap days to start at day 1
    day1 = ghi_ratio.index[0]
    ghi_ratio.index = ghi_ratio.index + pd.tseries.frequencies.to_offset('1D')
    # set day 1 estimated air temp equal to last day
    ghi_ratio[day1] = ghi_ratio.iloc[-1]
    # fix day 1 is added last, so out of order
    ghi_ratio = ghi_ratio.sort_index()
    # scale daily temperature delta by the ratio of insolation from day before
    temp_adj = (ghi_ratio - 1.0)*daily_delta_temp[ghi_ratio.index]  # use next day
    # where GHI ratio is not finite, use unadjusted clear sky temp
    temp_adj = temp_adj.where(ghi_ratio>0, 0)
    temp_adj = temp_adj.rename('temp_adj')
    # interpolate smoothly, but fill forward minutes in last day
    est_air_temp = pd.concat(
        [cs_temp_air,
         ghi_ratio.resample('1min').interpolate(),
         temp_adj.resample('1min').interpolate()], axis=1).pad()
    # Tadj = Tcs + (GHI/CS_GHI - 1) * DeltaT 
    # if GHI/CS_GHI > 1 then adjustment > DeltaT
    est_air_temp['Adjusted Temp (C)'] = (
        est_air_temp['Clear Sky Temperature (C)'] + est_air_temp.temp_adj)
    return est_air_temp, temp_adj, ghi_ratio, daily_delta_temp, cs_temp_air


if __name__ == "__main__":
    # do stuff
    # 2005
    #weather_years = list(weather_path.iterdir())
    #df, header = read_surfrad_year(weather_years[10])
    #df.head()