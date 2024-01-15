user_struct = lambda x: {"role": "user", "content": x}
system_struct = lambda x: {"role": "system", "content": x}
assistant_struct = lambda x: {"role": "assistant", "content": x}


def readf(path):
    with open(path) as f:
        return f.read()

def writef(path, text):
    with open(path, 'w') as f:
        return f.write(text)

