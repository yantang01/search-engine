import json
import os


def get_dirname(full):
    start = full.rfind("/")
    end = full.rfind(".html")
    dirname = full[start + 1:end]
    file_path = os.path.join("data", dirname)
    return file_path


def read_file(dirname, filename):
    file_path = os.path.join(dirname, filename)
    f = open(file_path, "r")
    data = f.read()
    js = json.loads(data)
    f.close()
    return js


def write_to_file(dirname, filename, content):
    file_path = os.path.join(dirname, filename)
    fileout = open(file_path, "w")
    fileout.write(json.dumps(content))
    fileout.close()
