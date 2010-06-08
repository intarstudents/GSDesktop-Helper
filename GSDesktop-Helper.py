#!/usr/bin/env python
# - coding: utf-8 -

import gtk
import keybinder

class GSDesktop_Helper:
  def __init__(self):
    
    self._hotkeys = {
      '<Ctrl>period'          : "next",           # Ctrl + .
      '<Ctrl>comma'           : "previous",       # Ctrl + ,
      '<Ctrl>equal'           : "playpause",      # Ctrl + =
      '<Ctrl>grave'           : "shuffle",        # Ctrl + `
      '<Ctrl>slash'           : "showsongtoast",  # Ctrl + /
      '<Ctrl>backslash'       : "togglefavorite", # Ctrl + \
      '<Ctrl><Alt>Page_Up'    : "volumeup",       # Ctrl + Alt + Page Up
      '<Ctrl><Alt>Page_Down'  : "volumedown",     # Ctrl + Alt + Page Down
    }
    
    for keystring in self._hotkeys:
      try:
        keybinder.bind(keystring, self.keyboard_callback, self._hotkeys[keystring])
      except Exception, e:
        print e
    
    self._window = gtk.Window()
    self._window.connect('destroy', gtk.main_quit)
    
    self._window.show_all()
    gtk.main()
    
  def keyboard_callback(self, toggle):
    print user_data

if __name__ == '__main__':
  GSDesktop_Helper()
