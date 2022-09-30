import sys

def read_stdin():
    return sys.stdin.buffer.read().split(b'\xff', 1)

def vernam_encrypt_decrypt(input, key):
    ciphertext = ""
    for i in range(len(input)):
        ciphertext += chr(input[i] ^ key[i % len(key)])
    return ciphertext

def main():
    sys.stdout.buffer.write(vernam_encrypt_decrypt(*read_stdin()).encode())

if __name__ == "__main__":
    main()