#!/usr/bin/env python
# - coding: utf-8 -

import os
import re
import gtk
import keybinder

class GSDesktop_Helper:
  def __init__(self):
    
    self._homedir = "%s/.appdata" % os.path.expanduser('~')
    self._appdata = os.listdir(self._homedir)
    self._shortcutAction = None
    
    for name in self._appdata:
      m = re.match("^(GroovesharkDesktop[A-Z0-9\.]+)$", name)
      
      if m:
        self._shortcutAction = "%s/%s/Local Store/shortcutAction.txt" % (self._homedir, m.group(0))
        
        if os.path.exists(self._shortcutAction):
          break
        else:
          self._shortcutAction = None
    
    if not self._shortcutAction:
      print "No shortcut action file!"
    
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
    if os.path.exists(self._shortcutAction) and os.access(self._shortcutAction, os.W_OK):
      file = open(self._shortcutAction, "a")
      file.write("%s\n" % toggle)
      file.close()
      print toggle

if __name__ == '__main__':
  GSDesktop_Helper()
