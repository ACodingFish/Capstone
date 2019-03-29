from distutils.core import setup, Extension
mod_name = "sensors_c"
module1 = Extension(mod_name, sources=["sensors.c"])
setup(name = mod_name, version = '1.0', ext_modules = [module1],
description = "This is for Sensor Monitoring")
