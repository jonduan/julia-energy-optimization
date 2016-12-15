#!/usr/bin/python

print "Calculador de panel solar de cerros de vera"

import pvlib
from pvlib.pvsystem import LocalizedPVSystem
import datetime
import pandas as pd
import scipy

latitude = -31.601
longitude = -56.813
altitude = 160
timezone = 'Etc/GMT+3'

sandia_modules = pvlib.pvsystem.retrieve_sam('cecmod')
sapm_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
module = sandia_modules['Suntech_Power_STP290_24_Vd']
inverter = sapm_inverters['SMA_America__STP20000TL_US_10__480V__480V__CEC_2013_'] #es el mas parecido que encontre

localized_system = LocalizedPVSystem(module_parameters=module,
				     inverter_parameters=inverter,
				     surface_tilt=latitude,
                                     surface_azimuth=0,
                                     latitude=latitude,
                                     longitude=longitude,
                                     name="Cerros de Vera",
                                     altitude=altitude,
                                     tz=timezone)

naive_times = pd.DatetimeIndex(start='20161213', end='20161214', freq='1h')
times = naive_times.tz_localize(timezone)
clearsky = localized_system.get_clearsky(times)

print("Clearsky radiation:")
print(clearsky)
print("-----------------------------------")

solar_position = localized_system.get_solarposition(times)

print("Solar Position:")
print(solar_position)
print("-----------------------------------")


total_irrad = localized_system.get_irradiance(solar_position['apparent_zenith'],
                                              solar_position['azimuth'],
                                              clearsky['dni'],
                                              clearsky['ghi'],
                                              clearsky['dhi'])

print("Total irradiance:")
print(total_irrad)
print("-----------------------------------")

temps = localized_system.sapm_celltemp(total_irrad['poa_global'],
                                       0, 30)
print("Temps:")
print(temps)
print("-----------------------------------")

aoi = localized_system.get_aoi(solar_position['apparent_zenith'],
                               solar_position['azimuth'])
print("AOI:")
print(aoi)
print("-----------------------------------")

airmass = localized_system.get_airmass(solar_position=solar_position)

print("Air masses:")
print(airmass)
print("-----------------------------------")

#effective_irradiance = localized_system.sapm_effective_irradiance(total_irrad['poa_direct'], 
#	total_irrad['poa_diffuse'],airmass['airmass_absolute'], aoi)

effective_irradiance = localized_system.calcparams_desoto(total_irrad['poa_global'],temps['temp_cell'],localized_system.module_parameters.alpha_sc)

print("Eff. irradiance:")
print(effective_irradiance)
print("-----------------------------------")

dc = localized_system.sapm(effective_irradiance, temps['temp_cell'])
ac = localized_system.snlinverter(dc['v_mp'], dc['p_mp'])
print(ac)
day_energy = ac.sum()
print("Total del dia: %f" % day_energy)
#annual_energy = ac.sum()
#energies[name] = annual_energy

