"""A Pyrex wrapper for the aspell api.

Pyrex is ****SO**** great! I wrote this in about 1 hour from the
Aspell doc. I spent most of that hour figuring out that I needed to
set the Aspell "prefix" to get it to work!

Intended usage is:

1) create a spell_checker object for each document.

2) check a word by calling the check method

3) if you get 0 back indicating a misspelling, use the suggest method
   to get a list of possible correct spellings.
   
4) tell aspell about the correct choice so it can learn from your
   errors using the store_replacement method
   
5) add words to either the session dictionary or to your personal
   dictionary using the add_to_session or add_to_personal methods.

import aspell
sc = aspell.spell_checker()
word = 'flarg'
if not sc.check(word):
  print word, 'is incorrect'
  print 'suggestions include:', sc.suggest(word)

To get this to build and work on Windows I downloaded the Windows
version of aspell from http://aspell.net/win32/. I got the Full
Installer, a dictionary, and the libraries for MS VisualC++ as
separate downloads. I let the first two go to their default locations
and I unpacked the zip file for the last into the C:\Program
Files\Aspell top directory. Then I copied the aspell-15.dll from
C:\Program Files\Aspell\bin to a folder on my path.

You will also, of course, need Pyrex from
http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/.

With the above completed the standard 'python setup.py install' should
build and install the extension.

I believe this should work on Linux with trivial modification.

This software is free for anyone to use for any purpose. If you or your
lawyer are stupid enough to believe that I have any liability for this
code then do not use it.

23 May 2004
Gary Bishop

"""

cdef extern from "aspell.h":
  ctypedef struct AspellConfig
  AspellConfig* new_aspell_config()
  void delete_aspell_config(AspellConfig*)
  int aspell_config_replace(AspellConfig*, char*, char*)
  ctypedef struct AspellCanHaveError
  AspellCanHaveError* new_aspell_speller(AspellConfig*)
  #ctypedef struct AspellManager
  unsigned int aspell_error_number(AspellCanHaveError*)
  char* aspell_error_message(AspellCanHaveError*)
  ctypedef struct AspellSpeller
  AspellSpeller* to_aspell_speller(AspellCanHaveError*)
  int aspell_speller_check(AspellSpeller*, char*, int)
  ctypedef struct AspellWordList
  AspellWordList* aspell_speller_suggest(AspellSpeller*, char*, int)
  ctypedef struct AspellStringEnumeration
  AspellStringEnumeration * aspell_word_list_elements(AspellWordList*)
  char* aspell_string_enumeration_next(AspellStringEnumeration*)
  int aspell_speller_store_replacement(AspellSpeller*, char*, int, char*, int)
  int aspell_speller_add_to_session(AspellSpeller*, char*, int)
  int aspell_speller_add_to_personal(AspellSpeller*, char*, int)
  int aspell_speller_error(AspellSpeller*)
  char* aspell_speller_error_message(AspellSpeller*)
  int aspell_speller_save_all_word_lists(AspellSpeller*)

class Error(Exception):
  pass

cdef class spell_checker:
  '''A simple wrapper for the Aspell API'''
  cdef AspellConfig* config
  cdef AspellSpeller* checker
  
  def __init__(self, lang="en_US", prefix="c:/Program Files/Aspell", **kwargs):
    self.config = new_aspell_config()
    aspell_config_replace(self.config, "prefix", prefix)
    aspell_config_replace(self.config, "lang", lang)
    for key,value in kwargs.items():
      aspell_config_replace(self.config, key, value)
    cdef AspellCanHaveError* possible_err
    possible_err = new_aspell_speller(self.config)
    if aspell_error_number(possible_err) != 0:
      msg = aspell_error_message(possible_err)
      raise Error, msg
    else:
      self.checker = to_aspell_speller(possible_err)

  def check(self, word):
    '''Return 0 if word is misspelled, 1 otherwise.'''
    return aspell_speller_check(self.checker, word, len(word))

  def suggest(self, word):
    '''Return a list of suggested replacements for a misspelled word.'''
    cdef AspellWordList* suggestions
    # I need a cast here to stop the C compiler from complaining about const mismatch
    suggestions = <AspellWordList*>aspell_speller_suggest(self.checker, word, len(word))
    cdef AspellStringEnumeration* elements
    elements = aspell_word_list_elements(suggestions)
    result = []
    cdef char* suggestion
    while 1:
      # this cast is the hush the C compiler which knows this function is const char*
      suggestion = <char*>aspell_string_enumeration_next(elements)
      if suggestion == NULL:
        break
      result.append(suggestion)
    return result

  def store_replacement(self, wrongword, rightword):
    '''Tell Aspell about the correction so it can learn about your mistakes.'''
    return aspell_speller_store_replacement(self.checker, wrongword, len(wrongword),
                                            rightword, len(rightword))

  def add_to_session(self, word):
    '''Tell Aspell to allow word for this session.'''
    return aspell_speller_add_to_session(self.checker, word, len(word))

  def add_to_personal(self, word):
    '''Tell Aspell to allow word permanently.'''
    r = aspell_speller_add_to_personal(self.checker, word, len(word))
    aspell_speller_save_all_word_lists(self.checker)
    return r

  
      


      
      
