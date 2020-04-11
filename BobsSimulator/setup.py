# cython: language_level=3, boundscheck=False
from setuptools import setup
from Cython.Build import cythonize


setup(
    ext_modules=cythonize("helloworld.pyx", compiler_directives={'language_level': 3}),
    zip_safe=False,
)
