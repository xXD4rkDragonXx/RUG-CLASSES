# vignere cipher

import sys


def charLower(char):
  return char.lower()

def encryptVignere(plain_text, key):
    cipher_text = ""
    j = 0
    for i in range(len(plain_text)):
        if plain_text[i].isalpha():
            if plain_text[i].isupper():
                cipher_text += chr((ord(charLower(plain_text[i])) + ord(charLower(key[j % len(key)])) - 194) % 26 + 97).upper()
            else:
                cipher_text += chr((ord(plain_text[i]) + ord(key[j % len(key)]) - 194) % 26 + 97)
            j += 1
        else:
            cipher_text += plain_text[i]
    return cipher_text

def decryptVignere(cipher_text, key):
    plain_text = ""
    j = 0
    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            if cipher_text[i].isupper():
                plain_text += chr((ord(charLower(cipher_text[i])) - ord(charLower(key[j % len(key)])) - 130) % 26 + 97).upper()
            else:
                plain_text += chr((ord(cipher_text[i]) - ord(key[j % len(key)]) - 130) % 26 + 97)
            j += 1
        else:
            plain_text += cipher_text[i]
    return plain_text

# handle input
def handle_input(query, input_text):
    steps = query.split(" ")
    for i in range(0, len(steps), 2):
        if steps[i] == "d":
            handled_input = decryptVignere(input_text, steps[i+1])
        elif steps[i] == "e":
            handled_input = encryptVignere(input_text, steps[i+1])
        input_text = handled_input
    return handled_input


def main():

    # # get lines from file
    # with open("2.in.txt", "r") as f:
    #     lines = f.readlines()

    # # get query
    # query = lines[0].strip()

    # input_text = []
    # # get input text
    # for lines in lines[1:]:
    #     input_text.append(lines.strip())

    input_text = []
    for line in sys.stdin:
        # get first line
        if line.startswith("e") or line.startswith("d"):
            query = line.rstrip()
        # get other lines
        else:
            input_text.append(line.rstrip())


    for lines in input_text:
        if len(input_text) > 2:
            raise Exception(input_text)
        print(handle_input(query, lines))

if __name__ == "__main__":
    main()