#from distutils.core import setup
from setuptools import setup, Extension
from os.path import exists
from subprocess import call

lz = Extension('dsts.lz', include_dirs=['dsts/external/dstc/lzOG/src/', 'dsts/external/dstc/SAIS-SK/src/'],
               sources=['dsts/lzmodule.cpp', 'dsts/external/dstsc/lzOG/src/lzOG.cpp', 'dsts/external/dstsc/SAIS-SK/src/mmap.cpp',
                        'dsts/external/dstsc/SAIS-SK/src/fileopen.cpp', 'dsts/external/dstsc/SAIS-SK/src/gt-alloc.cpp',
                        'dsts/external/dstsc/SAIS-SK/src/sk-sain.cpp'])

# When this script is run, we want to unsure that the distc package is installed
# The distc package has C++ code that is required when building the lz extension
if not exists("dsts/external/dstsc/SAIS-SK/") or not exists("dsts/external/dstsc/lzOG/"):
    call(["git", "submodule", "foreach", "git", "pull"])

setup(name="dsts",
      version="0.6",
      description="Python data structures.",
      author="Angelos Molfetas",
      author_email="angelos.molfetas@unimelb.edu.au",
      packages=['dsts'],
      long_description="Python data structures. Suffix array Construction Algorithm, Rabin & Karp fingerprint generator, LZ factorisor.",
      ext_modules=[lz],
      )
