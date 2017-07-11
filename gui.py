import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import glade

handlers = {
    'onDeleteWindow': Gtk.main_quit
}

builder = Gtk.Builder()
builder.add_from_file(glade.GUI_MAIN)
builder.add_from_file(glade.GUI_OPEN)
builder.add_from_file(glade.GUI_CLOSE)
builder.add_from_file(glade.GUI_CREATE)
builder.connect_signals(handlers)

main_window = builder.get_object('main_window')
notebook = builder.get_object('notebook')

#Tabs labels
open_label = Gtk.Label('Open')
close_label = Gtk.Label('Close')
create_label = Gtk.Label('Create')

#Add tabs
gui_open = builder.get_object('gui_open')
gui_close = builder.get_object('gui_close')
gui_create = builder.get_object('gui_create')
notebook.append_page(gui_open, open_label)
notebook.append_page(gui_close, close_label)
notebook.append_page(gui_create, create_label)

main_window.show_all()

Gtk.main()
