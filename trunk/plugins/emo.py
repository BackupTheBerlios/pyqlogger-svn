import sys,os,xml.dom.minidom,pickle

print "Kopete EmotIcon Theme Converter for PyQLogger."
if len(sys.argv)<3:
    print "Usage: emo_conv.py [source dir] [target file] [prefix url]"
    print "Where:"
    print "[source dir] is the name of directory that hold Emotion Icon theme from Kopete"
    print "[target file] is the name of smiley theme file for PyQlogger that will be created"
    print "[prefix url] is the url that where the icons are stored. should include slash at the end"
    sys.exit()

sdir = sys.argv[1]
try:
    f = open(sdir+"/emoticons.xml","r")
    fo = open(sys.argv[2],"w")
except:
    print "One of the files couldn't be opened!"
    sys.exit()
    
prefixurl = sys.argv[3]
parser = xml.dom.minidom.parse(f)
smiles = []
if len(parser.childNodes)<1 or parser.childNodes[0].nodeName != u'messaging-emoticon-map':
    print "bad file! bad!"
    sys.exit()
else:
    for node in parser.childNodes[0].childNodes:
        if node.nodeName != u'emoticon': continue
        s = {}
        s["name"] = node.attributes['file'].value
        imgf = open("%s/%s.png"%(sdir,s["name"]),"rb")
        s["image"] = pickle.dumps(imgf.read())
        imgf.close()
        s["url"] = "%s%s.png"%(prefixurl,s["name"])
        s["variants"] = []
        for subnode in node.childNodes:
            if subnode.nodeName != u'string': continue
            s["variants"] += [ subnode.childNodes[0].nodeValue ]
        smiles += [ s ]
pickle.dump(smiles,fo)        
f.close()
fo.close()
print "Thank you and come again!"
