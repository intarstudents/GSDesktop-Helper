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
    
    # Default list of all hotkeys and their actions
    self._hotkeys = {
      "next"            : "<Ctrl>period",         # Ctrl + .
      "previous"        : "<Ctrl>comma",          # Ctrl + ,
      "playpause"       : "<Ctrl>equal",          # Ctrl + =
      "shuffle"         : "<Ctrl>grave",          # Ctrl + `
      "showsongtoast"   : "<Ctrl>slash",          # Ctrl + /
      "togglefavorite"  : "<Ctrl>backslash",      # Ctrl + \
      "volumeup"        : "<Ctrl><Alt>Page_Up",   # Ctrl + Alt + Page Up
      "volumedown"      : "<Ctrl><Alt>Page_Down", # Ctrl + Alt + Page Down
    }
    
    self._hotkey_name = {
      "next"            : "Plays next song",
      "previous"        : "Plays previous song",
      "playpause"       : "Toggles Play/Pause",
      "shuffle"         : "Toggles Shuffle",
      "showsongtoast"   : "Displays song info",
      "togglefavorite"  : "Favorites song",
      "volumeup"        : "Increases volume",
      "volumedown"      : "Decreases volume",
    }
    
    self.bindKeys()
    self.modify_toggle = None
    self.create_conf_window()
    
    # Status icon stuff
    self._status_icon = gtk.StatusIcon()
    self._status_icon.set_from_file(self._ICON)
    self._status_icon.set_tooltip(self._NAME)
    self._status_icon.connect("popup-menu", self.menu_callback)
    
    gtk.main()
  
  def create_conf_window(self):
    self._window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    #self._window.set_resizable(False)
    self._window.set_title(self._NAME)
    self._window.set_default_size(460, 495)
    self._window.set_icon_from_file(self._ICON)
    self._window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    self._window.set_border_width(10)
    self._window.connect("destroy", self.hide_conf_window)
    
    self._confMainBox = gtk.VBox(False, 0)
    self._confRowBox  = gtk.VBox(False, 0)
    
    warningLabel = gtk.Label("These keyboard shortcuts will be unbinded while editing!")
    warningLabel.show()
    
    self._confRowBox.pack_start(warningLabel)
    
    for toggle in self._hotkeys:
      box = gtk.HBox(False, 0)
      
      seperator = gtk.Label("")
      seperator.show()
      
      label = gtk.Label(self._hotkey_name[toggle])
      label.set_justify(gtk.JUSTIFY_LEFT)
      label.show()
      
      keyval, state = gtk.accelerator_parse(self._hotkeys[toggle])
      mod = gtk.accelerator_get_label(keyval, state)
      
      entry = gtk.Entry()
      entry.set_editable(False)
      entry.set_text(mod)
      entry.toggle = toggle
      entry.connect("event", self.change_toggle)
      entry.show()
      
      box.pack_start(label, False, False, 0)
      box.pack_start(seperator)
      box.pack_start(entry, False, False, 0)
      box.show()
      
      self._confRowBox.pack_start(box, True, True, 0)
    
    self._confRowBox.show()
    self._window.add(self._confRowBox)
  
  def change_toggle(self, widget, event, data=None):
    if event.type == gtk.gdk.BUTTON_RELEASE:
      self.modify_toggle = widget.toggle
  
  def show_conf_window(self, window):
    self.unbindKeys()
    self._window.show()
  
  def hide_conf_window(self, window):
    self.bindKeys()
    self._window.hide()
  
  def bindKeys(self):
    for toggle in self._hotkeys:  
      try:  keybinder.unbind(self._hotkeys[toggle])
      except: pass
        
      try:
        keybinder.bind(self._hotkeys[toggle], self.keyboard_callback, toggle)
        print "%s binded" % self._hotkeys[toggle]
        
      except Exception, e:
        pass
  
  def unbindKeys(self):
    for toggle in self._hotkeys:  
      try:  keybinder.unbind(self._hotkeys[toggle])
      except: pass
  
  # Handle recieved hotkey action
  def keyboard_callback(self, toggle):
    if os.path.exists(self._shortcutAction) and os.access(self._shortcutAction, os.W_OK):
      print toggle
      try:
        file = open(self._shortcutAction, "a")
        file.write("%s\n" % toggle)
        file.close()
      except Exception, e:
        print e
  
  # Handle status icon popup
  def menu_callback(self, icon, button, time):
    menu = gtk.Menu()
    
    configure   = gtk.MenuItem("Configure")
    about   = gtk.MenuItem("About")
    quit    = gtk.MenuItem("Quit")
    
    configure.connect("activate", self.show_conf_window)
    about.connect("activate", self.show_about_dialog)
    quit.connect("activate", gtk.main_quit)
    
    menu.append(configure)
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
