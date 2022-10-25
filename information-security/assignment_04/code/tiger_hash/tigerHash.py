import sys

def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

def read_stdin():
    return sys.stdin.buffer.read()

def main():
    # this makes it possible to read from stdin when no filename is given on execution
    # execute with: python tigerHash.py [readfrom]
    if len(sys.argv) > 1:
        data = read_file(sys.argv[1])
    else:
        data = read_stdin()

    # TODO give output
    sys.stdout.buffer.write(data)

if __name__ == "__main__":
    main()