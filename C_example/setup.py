from distutils.core import setup, Extension
MOD = "benchmark"
setup(name = MOD, ext_modules = [Extension(MOD,sources=['benchmark.c'])],
description = "My C Extension Module")