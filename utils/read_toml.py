
from sys import argv
import toml


def read_toml():

    message = '\n\nUsage: read_toml.py <file> <key1> [<key2>] [<key3>] ...'

    if len(argv) < 2:
        raise ValueError("Error check usage below. " + message)
    if len(argv) == 2:
        raise ValueError("Only file specified. " + message)
    if len(argv) < 3:
        raise ValueError('No keys specified. ' + message)

    file = argv[1]
    nested_args = argv[2:]

    with open(file) as f:
        data = toml.load(f)

    for key in nested_args:
        data = data[key]

    print(data)

if __name__ == '__main__':
    read_toml()