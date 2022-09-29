import sys

# read binary input from stdin and split at first accurance of 0xFF
def read_stdin():
    return sys.stdin.buffer.read().split(b'\xff', 1)

# apply RC4 encryption on text using key
def rc4(key, text):
    # key scheduling
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    # pseudo-random generation
    # add 256 bytes to start of text
    text = bytes(S) + text
    i = j = 0
    keystream = []
    for _ in text:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])
    # xor keystream with text
    return bytes([c ^ k for c, k in zip(text, keystream)])[256:]

# return encrypted text
sys.stdout.buffer.write(rc4(*read_stdin()))
