import contextlib
import tempfile
import os
import shutil

@contextlib.contextmanager
def get_temp_path():
    original_wd = os.getcwd()

    path = tempfile.mkdtemp()

    try:
        os.chdir(path)

        yield path
    finally:
        os.chdir(original_wd)

        try:
            shutil.rmtree(path)
        except:
            pass

def populate_path(path, max_files=100, max_size=1024 * 1024):
    """Populate the path incrementing the sizes according to Fibonacci."""

    i = 0
    current_size = 0
    j, k = 1, 1
    while i < max_files and current_size < max_size:
        filepath = os.path.join(path, 'file{}'.format(i))
        with open(filepath, 'w') as f:
            f.seek(current_size)
            f.write('x')

        if i < 2:
            l = 1
        else:
            l = j + k
            j, k = k, l

        i += 1
        current_size = l
