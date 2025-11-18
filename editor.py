import os
from datetime import datetime

def create_file(filename):
    if os.path.exists(filename):
        raise FileExistsError("File already exists.")
    open(filename, "w", encoding="utf-8").close()
    print(f"File '{filename}' created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def read_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("File not found.")
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    print(f"File '{filename}' read at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return content

def write_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"File '{filename}' saved at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def delete_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError("File not found.")
    os.remove(filename)
    print(f"File '{filename}' deleted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def delete_content(filename):
    """Clears the file content but keeps the file."""
    if not os.path.exists(filename):
        raise FileNotFoundError("File not found.")
    open(filename, "w", encoding="utf-8").close()
    print(f"Content of '{filename}' deleted at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

