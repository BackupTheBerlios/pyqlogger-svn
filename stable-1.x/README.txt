$Id$

PyQLogger - PyQT Blogger Client by Reflog
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FEATURES:
~~~~~~~~~

* Simple and easy GUI
* Easy setup wizard
* Posts fetching from the blog for later editing and re-publishing
* Async and responsive UI
* Posts saving feature (drafts)
* On-Screen notifications of events
* Post editor with syntax highlighting (with optional QScintilla support)
* Post preview (with optional KHTML Support)
* Multiple blog support
* Post export
* Update notification (for pyqlogger itself)
* Pluggable features, like SpellChecker and others
* Unicode support
* Multiple blog providers
* Kde integration (optional)

USES:
~~~~~

PyQt - http://riverbankcomputing.co.uk/pyqt
PyKde - http://riverbankcomputing.co.uk/pykde
PyOSD - http://repose.cx/pyosd/
FeedParser - http://diveintomark.org/projects/feed_parser/


UNINSTALL:
~~~~~~~~~~

To manually remove PyQLogger from your system issue the following commands:
As user:
rm -rf ~/.pyqlogger
As root:
rm -rf /usr/share/pyqlogger
rm -rf /usr/lib/python2.3/site-packages/PyQLogger
rm -rf /usr/bin/pyqlogger.py
rm -rf /usr/share/applications/pyqlogger.desktop


Plugin Dependancies
~~~~~~~~~~~~~~~~~~~~

For SpellCheck plugin to work you need ASpell, and ASpell module for Python, which
you can get from http://prdownloads.sourceforge.net/uncpythontools/aspell-1.0.zip?download

For Smiley plugin you have to get a theme first. It can be imported from Kopete's smiley theme like this:

1. Select a theme (I chose Default)
2. Go to your webserver and upload all the .png files from the theme
3. Take note of url where png's are stored now, for example: http://myhost.com/images/
4. Run converter emo.py /usr/kde/3.3/share/apps/kopete/pics/emoticons/Default smiley.theme http://myhost.com/images/
5. Put smiley.theme into ~/.pyqlogger/plugins/







THANKS:
~~~~~~~
Detlev Offenbach for Eric3, the most excellent Python IDE: http://www.die-offenbachs.de/detlev/eric3.html
David Boddie and others at PyKDE mailing list for help with QSyntaxHighlighter
BerliOS project for hosting
Mark Pilgrim for FeedParser, PyTextile and his awesome book DiveIntoPython
Xander Soldaat, for his patches and words of encouragment
