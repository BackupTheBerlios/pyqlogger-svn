from distutils.core import setup, Extension
from Pyrex.Distutils import build_ext
import os

if os.name == 'nt':
  aspell_home = 'c:/Program Files/Aspell/aspell-dev-0-50-3-3'
  libraries = ['aspell-15']
else:
  aspell_home = '/usr'
  libraries = ['aspell']
  
include_dirs = [aspell_home+'/include']
library_dirs = [aspell_home+'/lib']
  

ext = Extension('aspell', ['aspell.pyx' ],
                libraries = libraries,
                include_dirs = include_dirs,
                library_dirs = library_dirs,
                )
                
setup(name="aspell", version="1.1",
      ext_modules = [ext],
      cmdclass = {'build_ext': build_ext}
)
