import lukr_manager
import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import glade

class MainWindow():
    
    def __init__(self):
        self.lukr = lukr_manager.LukrManager()
        self.builder = Gtk.Builder()
        self.builder.add_from_file(glade.GUI_MAIN)
        self.open_box = OpenBox(self)
        self.builder.add_from_file(glade.GUI_CLOSE)
        self.builder.add_from_file(glade.GUI_CREATE)
        #Tabs labels
        self.open_label = Gtk.Label('Open')
        self.close_label = Gtk.Label('Close')
        self.create_label = Gtk.Label('Create')
        
        self.builder.connect_signals(self)
        
        self.main_window = self.builder.get_object('main_window')
        self.notebook = self.builder.get_object('notebook')
        self.gui_open = self.builder.get_object('gui_open')
        self.gui_close = self.builder.get_object('gui_close')
        self.gui_create = self.builder.get_object('gui_create')
        
        self.notebook.append_page(self.gui_open, self.open_label)
        self.notebook.append_page(self.gui_close, self.close_label)
        self.notebook.append_page(self.gui_create, self.create_label)
        
    def onDeleteWindow(self, *args):
        return Gtk.main_quit(*args)
    
    def run(self):
        self.main_window.show_all()
        Gtk.main()

class OpenBox():

    def __init__(self, parent):
        self.parent = parent
        self.lukr = self.parent.lukr
        self.builder = self.parent.builder
        self.builder.add_from_file(glade.GUI_OPEN)
        
        name = 'open-encrypted-file-button'
        self.encrypted_file_button = self.builder.get_object(name)
        name = 'open-mount-point-button'
        self.mount_point_button = self.builder.get_object(name)
        
        #Connect signals
        args = 'clicked', self.handle_open_device
        self.builder.get_object('open-device-button').connect(*args)

    def handle_open_device(self, widget):
        self.lukr.open(self.encrypted_file_button.get_filename(),
                       self.mount_point_button.get_filename())
