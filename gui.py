import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import glade

handlers = {
    'onDeleteWindow': Gtk.main_quit
}

builder = Gtk.Builder()
builder.add_from_file(glade.GUI_MAIN)
builder.connect_signals(handlers)

main_window = builder.get_object('main_window')
main_window.show_all()

Gtk.main()
