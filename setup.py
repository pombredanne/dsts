#from distutils.core import setup
from setuptools import setup, Extension

lz = Extension('dsts.lz', include_dirs=['dsts/external/dstc/lzOG/src/', 'dsts/external/dstc/SAIS-SK/src/'],
               sources=['dsts/lzmodule.cpp', 'dsts/external/dstsc/lzOG/src/lzOG.cpp', 'dsts/external/dstsc/SAIS-SK/src/mmap.cpp',
                        'dsts/external/dstsc/SAIS-SK/src/fileopen.cpp', 'dsts/external/dstsc/SAIS-SK/src/gt-alloc.cpp',
                        'dsts/external/dstsc/SAIS-SK/src/sk-sain.cpp'])

setup(name="dsts",
      version="0.6",
      description="Python data structures.",
      author="Angelos Molfetas",
      author_email="angelos.molfetas@unimelb.edu.au",
      packages=['dsts'],
      long_description="Python data structures. Suffix array Construction Algorithm, Rabin & Karp fingerprint generator, LZ factorisor.",
      ext_modules=[lz],
      )
