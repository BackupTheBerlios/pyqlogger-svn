Installation
~~~~~~~~~~~~

This is trivial. Copy the .tar.gz file to ~/.pyqlogger
Then type 'tar xvfz plugins.tar.gz'

And that's it!

Dependancies
~~~~~~~~~~~~

For SpellCheck plugin to work you need ASpell, and ASpell module for Python, which
you can get from http://prdownloads.sourceforge.net/uncpythontools/aspell-1.0.zip?download

For Smiley plugin you have to get a theme first. It can be imported from Kopete's smiley theme like this:

1. Select a theme (I chose Default)
2. Go to your webserver and upload all the .png files from the theme
3. Take note of url where png's are stored now, for example: http://myhost.com/images/
4. Run converter emo.py /usr/kde/3.3/share/apps/kopete/pics/emoticons/Default smiley.theme http://myhost.com/images/
5. Put smiley.theme into ~/.pyqlogger/plugins/
