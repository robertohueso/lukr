import functools
import os.path

GLADE_DIR = os.path.join(os.path.dirname(__file__), './glade/')
get = functools.partial(os.path.join, GLADE_DIR)

GUI_MAIN = get('main.glade')
