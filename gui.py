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
        self.close_box = CloseBox(self)
        self.create_box = CreateBox(self)
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
        device = [self.encrypted_file_button.get_filename(),
                  self.mount_point_button.get_filename()]
        self.lukr.open(*device)
        CloseBox.opened_list.append(device)

class CloseBox():
    
    opened_list = Gtk.ListStore(str, str)
    
    def __init__(self, parent):
        self.parent = parent
        self.lukr = self.parent.lukr
        self.builder = self.parent.builder
        self.builder.add_from_file(glade.GUI_CLOSE)
        
        name = 'opened-tree-view'
        self.opened_tw = self.builder.get_object(name)
        name = 'opened-tree-view-selection'
        self.opened_tw_selection = self.builder.get_object(name)
        
        #Connect signals
        args = 'clicked', self.handle_close_device
        self.builder.get_object('close-device-button').connect(*args)
        #Set TreeView
        self.opened_tw.set_model(CloseBox.opened_list)
        renderer = Gtk.CellRendererText()
        device_column = Gtk.TreeViewColumn('Encrypted device', renderer, text=0)
        mount_column = Gtk.TreeViewColumn('Mount point', renderer, text=0)
        self.opened_tw.append_column(device_column)
        self.opened_tw.append_column(mount_column)

    def handle_close_device(self, widget):
        model, m_iter = self.opened_tw_selection.get_selected()
        selection = model[m_iter]
        self.lukr.close(selection[0], selection[1])
        CloseBox.opened_list.remove(m_iter)

class CreateBox():
    
    def __init__(self, parent):
        self.parent = parent
        self.lukr = self.parent.lukr
        self.builder = self.parent.builder
        self.builder.add_from_file(glade.GUI_CREATE)
        
        name = 'file-chooser-button'
        self.file_chooser_btn = self.builder.get_object(name)
        name = 'size-entry'
        self.size_entry = self.builder.get_object(name)
        name = 'random-switch'
        self.random_switch = self.builder.get_object(name)
        name = 'create-button'
        self.create_btn = self.builder.get_object(name)
        
        #Connect signals
        args = 'clicked', self.handle_save_file
        self.file_chooser_btn.connect(*args)
        args = 'clicked', self.handle_create_device
        self.create_btn.connect(*args)

    def handle_save_file(self, widget):
        dialog = Gtk.FileChooserDialog("Save your device",
                                       None,
                                       Gtk.FileChooserAction.SAVE,
                                       (Gtk.STOCK_CANCEL,
                                        Gtk.ResponseType.CANCEL,
                                        'Save',
                                        Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.new_file = dialog.get_filename()
        dialog.destroy()

    def handle_create_device(self, widget):
        new_file = self.new_file
        size = self.size_entry.get_text()
        random = self.random_switch.get_active()
        self.lukr.create(new_file, size, random)
