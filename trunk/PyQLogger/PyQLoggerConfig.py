## $Id$
## This file is part of PyQLogger.
## 
## Copyright (c) 2004 Eli Yukelzon a.k.a Reflog &
##                    Xander Soldaat a.k.a. Mightor
##
## PyQLogger is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## PyQLogger is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with PyQLogger; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##
import os
import pickle
from ConfigParser import ConfigParser

class PyQLoggerConfig (ConfigParser):
    
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults)

    def read(self, configfile):
    # do some checking to see if there's a new style file available
    # if not, check if there's an old one.
        if not os.path.exists(configfile):
            if os.path.exists(configfile[0:-4]):
                self.convert_config(configfile)
        # convert_config will write the file, so reread it
        ConfigParser.read(self, configfile)

    def convert_config(self, configfile):
        """ unpickles the specified file into a hash """
        config_hash = None
        try:
            fd = open(configfile[0:-4])
            config_hash = pickle.load(fd)
            fd.close()
        except:
            return
    
        # This is soooooo nasty, way too many if statements....
        for key in config_hash.keys():
            if key == "blogs":
                if len(config_hash["blogs"]) > 0:
                    bloglist = config_hash["blogs"]
                    for blogname in bloglist.keys():
                        blogentry = bloglist[blogname]
                        blogid = blogentry["id"]
                        if not self.has_section(blogid):
                            self.add_section(blogid)
                        if blogname == config_hash["selectedblog"]:
                            if not self.has_section("main"):
                                self.add_section("main")
                            self.set("main", "selectedblog", blogid)
                        self.set(blogid, "name", blogname)
                    for blogkey in blogentry.keys():
                        self.set(blogid, blogkey, blogentry[blogkey])
            else: 
                if not self.has_section("main"):
                    self.add_section("main")
                if key != "selectedblog":
                    self.set("main",key, config_hash[key])
        
        try:
            fd = open(configfile, "w")
            self.write(fd)
            fd.close()
        except:
            pass
        return

    def savesettings(self, configfile):
        try:
            fd = open(configfile, "w")
            self.write(fd)
            fp.close()
        except:
            # We need better error handling here, user needs to be notified
            pass
        return
