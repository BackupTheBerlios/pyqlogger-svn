# Class inspired by code from Chris Thomson and Sebastien Keim
import popen2, Cache, re, string

class aspell:
    """ Simple ASpell Pipe client, with results caching """

    def __init__(self, prefix="/usr/bin", lang=None):
        """ initialize a cache, and regexp for parsing aspell results """
        self._f = popen2.Popen3("%s/aspell -a"%prefix)
        self._f.fromchild.readline() #skip the credit line
        self.words = Cache.Cache(100)
        self.parse = re.compile("^[&\?] \w+ [0-9]+ [0-9]+:(.*?)$", re.M)

    def add(self, word):
        """ add word to user dictionary """
        self._f.tochild.write("&"+word+'\n')
        self._f.tochild.flush()

    def ignore(self, word):
        """ temporary ignore the word """
        self._f.tochild.write("@"+word+'\n')
        self._f.tochild.flush()
        self.words[word] = None

    def suggest(self, word):
        """
        checks the word in aspell.
        returns: None if word is correct ,
        [] if cannot suggest anything or a list of suggestions
        """
        if word in self.words:
            return self.words[word]
        self._f.tochild.write(word+'\n')
        self._f.tochild.flush()
        s = self._f.fromchild.readline()
        self._f.fromchild.readline() #skip the blank line
        if s[:1]=="*" or s[:1]=="+" or s[:1]=="-":
            res = None
        elif s[0]=="#":
            res = []
        else:
            m = self.parse.search("\n"+s, 1)
            if m:
                res = map(string.strip,(m.group(1).split(', ')))
            else:
                print "wtf: " + s
                res = []
        self.words[word] = res
        return res

if __name__ == "__main__":
    f = aspell()
    print f.suggest('hello')
    print f.suggest('stinge')
    print f.ignore('stinge')
    print f.suggest('reflog')
    print f.add('reflog')
    print f.suggest('stinge')

