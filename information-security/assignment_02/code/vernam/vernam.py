import sys

def read_stdin():
    return sys.stdin.buffer.read().split(b'\xff', 1)

def vernam_encrypt_decrypt(input, key):
    ciphertext = []
    for i in range(len(input)):
        ciphertext.append(input[i] ^ key[i % len(key)])
    return bytes(ciphertext)

def main():
    sys.stdout.buffer.write(vernam_encrypt_decrypt(*read_stdin()))

if __name__ == "__main__":
    main()