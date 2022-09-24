import sys


def encrypt(key, text):
    # encrypt text using given key
    counter = 0
    newText = []
    for i in range(len(text)):
        # continue if character is alphanumeric
        if text[i].isalpha():
            start = ord('A') if text[i].isupper() else ord('a')
            newText.append(chr(
                ((ord(text[i]) - start + ord(key[counter % len(key)]) - ord('a')) % 26) + start))
            counter += 1
        else:
            newText.append(text[i])
    print(''.join(newText))


def decrypt(key, text):
    # decrypt text using given key
    counter = 0
    newText = []
    for i in range(len(text)):
        # continue if character is alphanumeric
        if text[i].isalpha():
            start = ord('A') if text[i].isupper() else ord('a')
            newText.append(chr(
                ((ord(text[i]) - start - ord(key[counter % len(key)]) + ord('a')) % 26) + start))
            counter += 1
        else:
            newText.append(text[i])
    print(''.join(newText))


def handle_input(ende, key, input):
    if(ende == 'd'):
        decrypt(key, input)
    elif(ende == 'e'):
        encrypt(key, input)
    else:
        print("Invalid input")


def main():
    ende = ''
    key = ''
    input = ''
    # get input text
    for line in sys.stdin:
        if key == '':
            ende, key = line.strip().split(' ')
        elif line.strip() == '':
            handle_input(ende, key, input)
        else:
            input = input + line


if __name__ == "__main__":
    main()
