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
            fd = open(str(configfile[0:-4]))
            config_hash = pickle.load(fd)
            fd.close()
        except Exception, inst:
            print inst
            return
    
        for key in config_hash.keys():
            if key == "blogs":
                if len(config_hash["blogs"]) > 0:
                    bloglist = config_hash["blogs"]
                    self.delblogs()
                    self.addblogs(bloglist)
                    if config_hash.has_key("selectedblog"):
                        blogid = self.getblogID(unicode(config_hash["selectedblog"]))
                        self.set("main", "selectedblog", blogid)
            else: 
                self.add_section("main")
                if key != "selectedblog":
                    self.set("main",key, config_hash[key])
        
        try:
            fd = open(str(configfile), "w")
            self.write(fd)
            fd.close()
        except Exception, inst:
            print inst
            pass
        return

    def get(self, section, option):
        if self.has_section(section):
            if self.has_option(section, option):
                return ConfigParser.get(self, section, option)
        else:
            return None
    
    def add_section(self, section):
        if not self.has_section(section):
            ConfigParser.add_section(self, section)
    
    def set(self, section, option, value):
        if value or len(value) > 0:
            self.add_section(section)
            ConfigParser.set(self, section, option, value)
        else:
            print "PyQLoggerConfig.set(): NULL or 0 len value passed to section: %s, option: %s, value: %s" % (section, option, value)
            
    def savesettings(self, configfile):
        try:
            fd = open(configfile, "w")
            self.write(fd)
            fd.close()
        except Exception, inst:
            print "PyQLoggerConfig.savesettings: %s" % inst
            # We need better error handling here, user needs to be notified
            pass
        return
    
    def remove_section(self, section):
        try:
            ConfigParser.remove_section(self, section)
        except Exception, inst:
            print "PyQLoggerConfig.remove_section: %s" % inst
        
    def delblogs(self):
        blogids = str(self.get("main", "blogs"))
        if blogids:
            for blogid in blogids.split(';'):
                self.remove_section(blogid)
        self.remove_option("main", "blogs")
        self.remove_option("main", "selectedblog")
        
    def addblogs(self, blogdict):
        blogids = self.get("main", "blogs")
        if len(blogdict) < 1:
            return
        for blogname in blogdict.keys():
            blogentry = blogdict[blogname]
            blogid = blogentry["id"]
            blogids = self.get("main", "blogs")
            if blogids is None:
                self.set("main", "blogs", blogid)
            elif blogid in blogids.split(';'):
                pass
            elif len(blogids) > 0:
                blogids += ";" + blogid
                self.set("main", "blogs", blogids)
            else:
                print "PyQLoggerConfig.addblogs: shouldn't be here"

            self.set(blogid, "name", blogname)
            for blogkey in blogentry.keys():
                self.set(blogid, blogkey, blogentry[blogkey])

    def getblogID(self, blogname):
        if self.has_option("main", "blogs"):
            for blogid in self.get("main", "blogs").split(';'):
                if unicode(self.get(blogid, "name")) == unicode(blogname):
                    return blogid
    
    def getblogName(self, blogid):
        return self.get(blogid, "name")
