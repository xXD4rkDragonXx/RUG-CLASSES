import sys

# read binary input from stdin and split at first accurance of 0xFF


def read_stdin():
    return sys.stdin.buffer.read().split(b'\xFF', 2)

# read binary file


def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()


def f(part, keyPart):
    # returns key
    return bytes(keyPart)

def xor(a, b):
    # xor two byte arrays
    return bytes([a ^ b for a, b in zip(a, b)])

def feistel(key, text, encrypt=True):
    # split text into blocks of 8 bytes
    blocks = [text[i:i+8] for i in range(0, len(text), 8)]
    # devide key in blocks of 4 bytes
    keyBlocks = [key[i:i+4] for i in range(0, len(key), 4)]
    # encrypted text
    encrypted = b''
    for block in blocks:
        # split block in left and right part
        left = block[:4]
        right = block[4:]
        if encrypt:
            # encrypt
            for keyBlock in keyBlocks:
                left, right = right, xor(left, f(right, keyBlock))
        else:
            # decrypt
            # swap left and right part
            left, right = right, left
            for keyBlock in reversed(keyBlocks):
                left, right = right, xor(left, f(right, keyBlock))
            #  swap left and right part
            left, right = right, left
        # append left and right to encrypted text
        encrypted += left + right
    # return encrypted text
    return encrypted
            



# crypt, key, text = read_file('2.in.txt').split(b'\xFF', 2)
# print(feistel(key, text.replace(b'\r', b''), crypt == b'\x65').decode('utf-8'))

# return encrypted/decrypted text
crypt, key, text = read_stdin()
sys.stdout.buffer.write(feistel(key, text.replace(b'\r', b''), crypt == b'\x65'))
