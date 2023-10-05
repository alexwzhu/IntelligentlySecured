import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell



def find_notebook(filename, path=None):
    name = filename.split('.', 1)[-1]
    if not path:
        path = ['']
    for s in path:
        path2 = os.path.join(s, name + '.ipynb')
        if (os.path.isfile(path2)):
            return path2
        path2 = path2.replace("_", " ")
        if os.path.isfile(path2):
            return path2

class Loader(object):
    def __init__(s, path=None):
        s.shell = InteractiveShell.instance()
        s.path = path
    
    def load(s, filename):
        path = find_notebook(filename, s.path)
    
        print("importing notebook")

        with io.open(path, 'r', encoding='utf-8') as file:
            book = read(file, 4)
        
        module = types.ModuleType(filename)
        module.__file__ = path
        module.__loader__ = s
        module.__dict__['get_ipython'] = get_ipython
        sys.modules[filename] = module

        saved_user = s.shell.user_ns
        s.shell.user_ns = module.__dict__

        try:
            for c in book.cells:
                if c.cell_type == 'code':
                    code = s.shell.input_transformer_manager.transform_cell(c.source)
                    exec(code, module.__dict__)
        finally:
            s.shell.user_ns = saved_user
        return module

class Finder(object):
    def __init__(s):
        s.loaders = {}

    def find_module(s, filename, path=None):
        book_path = find_notebook(s, filename, path)
        if not book_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in s.loaders:
            s.loaders[key] = Loader(path)
        return s.loaders[key]
sys.meta_path.append(Finder())


def predict(pkt):
    return Model_Creation.predict(pkt)
    
