from contextlib import contextmanager


@contextmanager
def custom_open(filename: str, mode: str = 'w'):
    file_obj = open(filename, mode)
    yield file_obj
    file_obj.close()
