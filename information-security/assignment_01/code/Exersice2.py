import string


# substitution cypher

# Encrypts a string using a shift cypher
def encryptShift(plain_text, key):
    cipher_text = ""
    for char in plain_text:
        if char.isalpha():
            if char.isupper():
                cipher_text += chr((ord(char) + int(key) - 65) % 26 + 65)
            else:
                cipher_text += chr((ord(char) + int(key) - 97) % 26 + 97)
        else:
            cipher_text += char
    return cipher_text

# Decrypts a string using a shift cypher
def decryptShift(cipher_text, key):
    plain_text = ""
    for char in cipher_text:
        if char.isalpha():
            if char.isupper():
                plain_text += chr((ord(char) - int(key) - 65) % 26 + 65)
            else:
                plain_text += chr((ord(char) - int(key) - 97) % 26 + 97)
        else:
            plain_text += char
    return plain_text

# Encrypts a string using a mapping cypher
def encryptMapping(plain_text, mapping):
    cipher_text = ""
    for char in plain_text:
        if char.isalpha():
            if char.isupper():
                cipher_text += mapping[ord(char) - 65].upper()
            else:
                cipher_text += mapping[ord(char) - 97]
        else:
            cipher_text += char
    return cipher_text

# Decrypts a string using a mapping cypher
def decryptMapping(cipher_text, mapping):
    plain_text = ""
    for char in cipher_text:
        if char.isalpha():
            if char.isupper():
                plain_text += chr(mapping.index(char.lower()) + 97).upper()
            else:
                plain_text += chr(mapping.index(char) + 97)
        else:
            plain_text += char
    return plain_text

# Handles the input from the user
def handle_input(query):
    mappingoffset = string.ascii_lowercase
    steps = query.split(" ")
    for i in range(0, len(steps), 2):
        map_or_shift = stringToInt(steps[i+1])
        if steps[i] == "d":
            if isinstance(map_or_shift, int):
                mappingoffset = decryptShift(mappingoffset, map_or_shift)
            else:
                mappingoffset = decryptMapping(mappingoffset, map_or_shift)
        elif steps[i] == "e":
            if isinstance(map_or_shift, int):
                mappingoffset = encryptShift(mappingoffset, map_or_shift)
            else:
                mappingoffset = encryptMapping(mappingoffset, map_or_shift)
    return mappingoffset


# Converts a string to an int if possible
def stringToInt(string):
    try:
        value = int(string)
        return value
    except ValueError:
        return string

# Main function
def main():
    query = input()
    handled_input = handle_input(query)
    while(True):
        try:
            plain_text = input()
            print(encryptMapping(plain_text, handled_input))
        except EOFError:
            break

# Run main function
if __name__ == "__main__":
    main()