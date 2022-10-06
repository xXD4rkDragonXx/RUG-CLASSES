import sys

# read input file
def read_file(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()

# read input from stdin
def read_stdin():
    return sys.stdin.readlines()

# convert intput to object
def interpret_input(input):
    """
    Convert input to object.
    Returns object with keys 'encrypt', 'p', 'q', 'e' and 'numbers'.
    """
    # create object out of input
    inputObject = {
        'encrypt': True if input[0].strip() == 'e' else False,
        'p': 0,
        'q': 0,
        'e': 0,
        'numbers': list(map(int, [num.strip() for num in input[2:]]))
    }
    # get p, q and e from input line 2
    inputObject['p'], inputObject['q'], inputObject['e'] = list(map(int, input[1].strip().split(' ')))
    return inputObject

def calcPubKeyPartN(p, q):
    """
    calculate public key part n.
    Returns n, e.
    """
    # calculate n
    n = p * q
    return n

def calcPrivKey(p, q, e):
    """
    Calculate private key.
    Returns d.
    """
    # calculate phi
    phi = calcPhi(p, q)
    # calculate d
    d = extEuclid(e, phi)[1]
    # get positive d
    d = posD(d, phi)
    return d

def calcPhi(p, q):
    """
    Calculate phi.
    Returns phi.
    """
    phi = (p - 1) * (q - 1)
    return phi

def extEuclid(a, b):
    """
    calculates d, s, t such that d = gcd(a,b) and d == a*s + b*t
    Returns d, s and t.
    """
    if a == 0:
        return b, 0, 1
    else:
        d, t, x = extEuclid(b % a, a)
        return d, x - (b // a) * t, t

def posD(d, phi):
    """
    Returns positive d.
    """
    while d < 0:
        d = phi + d
    return d

def encrypt(numbers, e, n):
    """
    Encrypt numbers.
    Returns encrypted numbers.
    """
    encryptedNumbers = []
    for num in numbers:
        encryptedNumbers.append(pow(num, e, n))
    return encryptedNumbers

def decrypt(numbers, d, n):
    """
    Decrypt numbers.
    Returns decrypted numbers.
    """
    decryptedNumbers = []
    for num in numbers:
        decryptedNumbers.append(pow(num, d, n))
    return decryptedNumbers

# get input from file
input = interpret_input(read_file('in/9.in.txt'))

# get input from stdin
# input = interpret_input(read_stdin())

# get results and print them
N = calcPubKeyPartN(input['p'], input['q'])
nums = input['numbers']
if input['encrypt']:    
    e = input['e']
    print('\n'.join(map(str,encrypt(nums,e,N))))
else:
    P = calcPrivKey(input['p'], input['q'], input['e'])
    print('\n'.join(map(str,decrypt(nums,P,N))))