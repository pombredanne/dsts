#from distutils.core import setup
from setuptools import setup, Extension

module1 = Extension('hello', sources=['dsts/lzmodule.cpp'])

setup(name="dsts",
      version="0.5",
      description="Python data structures.",
      author="Angelos Molfetas",
      author_email="angelos.molfetas@unimelb.edu.au",
      packages=['dsts'],
      long_description="Python data structures. At the moment it only has a suffix array and a Rabin and Karp fingerprint generator.",
      ext_modules=[module1],
      )
