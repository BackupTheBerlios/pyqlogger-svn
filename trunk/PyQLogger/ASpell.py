# Class inspired by code from Chris Thomson and Sebastien Keim
import popen2, Cache, re, string

class aspell:
    """ Simple ASpell Pipe client, with results caching """

    def __init__(self, prefix="/usr/bin", lang=None):
        """ initialize a cache, and regexp for parsing aspell results """
        self._f = popen2.Popen3("%s/aspell -a"%prefix)
        s = self._f.fromchild.readline() #skip the credit line
        self.words = Cache.Cache(100)
        self.parse = re.compile("^[&\?] \w+ [0-9]+ [0-9]+: (.*?)$", re.M)

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
        s2 = self._f.fromchild.readline() #skip the blank line
        if s[0]=="*" or s[0]=="+" or s[0]=="-":
            res = None
        elif s[:1]=="#":
            res = []
        else:
            m = self.parse.search("\n"+s, 1)
            if m:
                res = map(string.strip,(m.group(1).split(', ')))
            else:
                res = []
        self.words[word] = res
        return res

if __name__ == "__main__":
    f = aspell()
    print "check hello and result: " + str(f.suggest('hello'))
    print "check helo and result: " + str(f.suggest('helo'))
    print "check reflogg and result: " + str(f.suggest('reflogg'))

