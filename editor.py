
import os
def create_file(filename):
    if os.path.exists(filename):
        raise FileExistsError("File already exists.")
    open(filename, "w", encoding="utf-8").close()


def read_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("File not found.")
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
