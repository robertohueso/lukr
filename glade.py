import functools
import os.path

GLADE_DIR = os.path.join(os.path.dirname(__file__), './glade/')
get = functools.partial(os.path.join, GLADE_DIR)

GUI_MAIN = get('main.glade')
GUI_OPEN = get('open.glade')
GUI_CLOSE = get('close.glade')
GUI_CREATE = get('create.glade')
