import pvlib
import pandas as pd


sandia_modules = pvlib.pvsystem.retrieve_sam('cecmod')

print('Paneles CEC')

for key, value in sandia_modules.iteritems() :
    print key

print('---------------------')
print('Inverters CEC')

sapm_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')
for key, value in sapm_inverters.iteritems() :
    print key

