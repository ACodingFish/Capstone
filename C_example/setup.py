from distutils.core import setup, Extension
mod_name = "benchmark"
module1 = Extension(mod_name, sources=["benchmark.c"])
setup(name = mod_name, version = '1.0', ext_modules = [module1],
description = "This is for a benchmark")
