# $Id$
"""PyQLogger: Multi-account Blog Client

User friendly and feature full Blog managment tool written in Python for posting to
Blogger, MovableType, LiveJournal and other blog provider. Has many nice features and
supports plugins.

"""

classifiers = """\
Development Status :: 4 - Beta
Intended Audience :: End Users/Desktop
License :: OSI Approved :: GNU General Public License (GPL)
Programming Language :: Python
Topic :: Internet
Topic :: Software Development :: Libraries :: Python Modules
Operating System :: Unix
"""
import sys,os,glob
from distutils.core import setup
import pyqlogger

if sys.version_info < (2, 3):
    _setup = setup
    def setup(**kwargs):
        if kwargs.has_key("classifiers"):
            del kwargs["classifiers"]
        _setup(**kwargs)

doclines = __doc__.split("\n")

setup(name="PyQLogger",
      version=pyqlogger.VERSION,
      maintainer="reflog",
      data_files=[ ('share/pyqlogger/plugins',glob.glob('plugins/*')), ("share/applications", ["pyqlogger.desktop"]) ],
      scripts=['pyqlogger.py'],
      packages=['PyQLogger'],
      maintainer_email="reflog@gmail.com",
      url = "http://pyqlogger.berlios.de/",
      download_url = "http://download.berlios.de/pyqlogger/PyQLogger-%s.tar.gz"%(pyqlogger.VERSION),
      license = "GPL",
      platforms = ["any"],
      description = doclines[0],
      classifiers = filter(None, classifiers.split("\n")),
      long_description = "\n".join(doclines[2:]),
      )
