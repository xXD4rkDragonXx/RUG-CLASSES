import sys

# read input from stdin
def read_stdin():
    return sys.stdin.readlines()

def interpret_input(input):
    # interpret input and create usable object
    if input[0].strip() == 'e':
        return {
            'crypt': 'e',
            'pub': [int(c) for c in input[1].strip().split(' ')],
            'ints': [int(c.strip()) for c in input[2:]]
        }
    elif input[0].strip() == 'd':
        return {
            'crypt': 'd',
            'm': int(input[1].split(' ')[0]),
            'n': int(input[1].split(' ')[1]),
            'sk': [int(c) for c in input[2].strip().split(' ')],
            'ints': [int(c.strip()) for c in input[3:]]
        }
    else:
        raise Exception('Invalid input')

def valToBoolArray(val):
    # convert integer to binary bool array
    return [int(c) for c in bin(val)[2:]] if val > 0 else [0]

def boolArrayToVal(array):
    # convert binary bool array to integer
    return int(''.join([str(c) for c in array]), 2)

def knap_encrypt(key, values):
    cipher = []
    # encrypt values using superincreasing knapsack
    for value in values:
        # convert value to reversed binary bool array
        value = valToBoolArray(value)[::-1]
        # encrypt value
        cipher.append(str(sum([key[i] * value[i] for i in range(len(value))])))
    # return encrypted values
    return cipher
        

def knap_decrypt(m, n, sk, values):
    # decrypt values using superincreasing knapsack
    modInv = pow(m, -1, n)
    results = []
    for value in values:
        # decrypt value
        result = (value * modInv) % n
        # calculate original value
        origVal = 0
        for val in sk[::-1]:
            if result >= val:
                result -= val
                origVal += 2 ** sk.index(val)
        # append original value to results
        results.append(str(origVal))    
    # return decrypted values
    return results        
            

def execute(input):
    # check if input is decrypt or encrypt
    if input['crypt'] == 'e':
        # encrypt
        return knap_encrypt(input['pub'], input['ints'])
    elif input['crypt'] == 'd':
        # decrypt
        return knap_decrypt(input['m'], input['n'], input['sk'], input['ints'])

# read input and print encrypted/decrypted text
input = read_stdin()
print('\n'.join(execute(interpret_input(input))))