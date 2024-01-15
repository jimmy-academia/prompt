import json

def readf(path):
    with open(path) as f:
        return f.read()

def writef(data, path):
    with open(path, 'w') as f:
        f.write(data)


def dumpj(data, path):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


user_struct = lambda x: {"role": "user", "content": x}
system_struct = lambda x: {"role": "system", "content": x}
assistant_struct = lambda x: {"role": "assistant", "content": x}
