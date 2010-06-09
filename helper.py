#!/usr/bin/env python
# - coding: utf-8 -

import os
import sys
import re
import gtk
import keybinder

class GSDesktop_Helper:
  def __init__(self):
    
    self._NAME    = "GSDesktop Helper"
    self._VERSION = "0.1"
    self._AUTHORS = ["Intars Students"]
    
    # Try to find icon file
    if os.path.exists("%s/gsd-helper.png" % sys.path[0]):
      self._ICON  = "%s/gsd-helper.png" % sys.path[0]
      
    elif os.path.exists("/usr/share/pixmaps/gsd-helper.png"):
      self._ICON  = "/usr/share/pixmaps/gsd-helper.png"
      
    else:
      # Else throw error and exit
      error_msg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Couldn't find icon file!")
      error_msg.run()
      
      error_msg.destroy()
      os._exit(0)
    
    # Find shortcutAction.txt file
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
      error_msg = gtk.MessageDialog(None, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, "Couldn't find shortcutAction.txt file!")
      error_msg.run()
      
      error_msg.destroy()
      os._exit(0)
    
    # List of all hotkeys and their actions
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
    
    # Bind all hotkeys (before making sure to unbind them)
    for keystring in self._hotkeys:  
      try:  keybinder.unbind(keystring)
      except: pass
        
      try:
        keybinder.bind(keystring, self.keyboard_callback, self._hotkeys[keystring])
        print "%s binded" % keystring
        
      except Exception, e:
        pass
    
    # Status icon stuff
    self._status_icon = gtk.StatusIcon()
    self._status_icon.set_from_file(self._ICON)
    self._status_icon.set_tooltip(self._NAME)
    self._status_icon.connect("popup-menu", self.menu_callback)
    
    gtk.main()
  
  # Handle recieved hotkey action
  def keyboard_callback(self, toggle):
    if os.path.exists(self._shortcutAction) and os.access(self._shortcutAction, os.W_OK):
      try:
        file = open(self._shortcutAction, "a")
        file.write("%s\n" % toggle)
        file.close()
      except Exception, e:
        print e
  
  # Handle status icon popup
  def menu_callback(self, icon, button, time):
    menu = gtk.Menu()

    about   = gtk.MenuItem("About")
    quit    = gtk.MenuItem("Quit")
    
    about.connect("activate", self.show_about_dialog)
    quit.connect("activate", gtk.main_quit)
    
    menu.append(about)
    menu.append(quit)
    
    menu.show_all()
    menu.popup(None, None, gtk.status_icon_position_menu, button, time, self._status_icon)
  
  # Show groovy About dialog
  def show_about_dialog(self, widget):
    
    about_dialog = gtk.AboutDialog()
    
    about_dialog.set_destroy_with_parent(True)
    about_dialog.set_name(self._NAME)
    
    about_dialog.set_version(self._VERSION)
    about_dialog.set_authors(self._AUTHORS)
    about_dialog.set_website("http://grooveshark.wikia.com/wiki/GSDesktop_Global_Keyboard_Shortcuts")
    about_dialog.set_website_label("How to groove?")
    
    icon = gtk.gdk.pixbuf_new_from_file(self._ICON)
    about_dialog.set_logo(icon)
    
    about_dialog.run()
    about_dialog.destroy()

if __name__ == '__main__':
  GSDesktop_Helper()
