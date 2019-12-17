#!/usr/bin/env python

# VEML6070 Driver Example Code
import UVHelper.veml6070 as veml6070

veml = veml6070.Veml6070()

for i in [veml6070.INTEGRATIONTIME_1_2T,
          veml6070.INTEGRATIONTIME_1T,
          veml6070.INTEGRATIONTIME_2T,
          veml6070.INTEGRATIONTIME_4T]:
  veml.set_integration_time(i)
  uv_raw = veml.get_uva_light_intensity_raw()
  uv = veml.get_uva_light_intensity()
  print "Integration Time setting %d: %f W/(m*m) from raw value %d" % (i, uv, uv_raw)
