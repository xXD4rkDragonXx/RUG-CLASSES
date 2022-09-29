import os
import sys

def vernam_encrypt_decrypt(input, key):
    ciphertext = ""
    for i in range(len(input)):
        ciphertext += chr(ord(input[i]) ^ ord(key[i % len(key)]))
    return ciphertext

def handle_file_input(filename="0.in.txt"):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    rel_path = "In\\" + filename
    abs_path = os.path.join(current_dir, rel_path)
    plaintext = ""
    key = ""
    with open(abs_path, "r") as file:
        filedata = ""
        for line in file:
            filedata += line
        inputs = filedata.split("\xFF")
        key = inputs[0]
        plaintext = inputs[1]
    return plaintext, key

def handle_input(data):
    inputs = data.split("\xFF")
    key = inputs[0]
    plaintext = inputs[1]
    return plaintext, key

def handle_output(ciphertext, filename="0.out"):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    rel_path = "Out\\" + filename
    abs_path = os.path.join(current_dir, rel_path)
    with open(abs_path, "r") as file:
        filedata = ""
        for line in file:
            filedata += line
        print("Output", filedata)
        print("Input", ciphertext)
        print(ciphertext == filedata)

def main():
    for i in range(0,4):
        fkey, input = handle_file_input(str(i) + ".in.txt")
        output = vernam_encrypt_decrypt(input, fkey)
        handle_output(output, str(i) + ".out")

    while True:
        data = sys.stdin.buffer.read()
        input, key = handle_input(data)
        output = vernam_encrypt_decrypt(input, key)
        print(output)

if __name__ == "__main__":
    main()