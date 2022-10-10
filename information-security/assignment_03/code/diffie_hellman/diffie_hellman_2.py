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
    Returns object with keys 'coords', 'a', 'b', 'p', 'm' and n.
    """
    # create object
    inputObject = {
        'coords': [],
        'a': 0,
        'b': 0,
        'p': 0,
        'm': 0,
        'n': 0
    }
    # read input and give values to object
    inputObject['coords'] = [*map(int, input[0].strip().replace('(', '').replace(')', '').split(', '))]
    inputObject['a'], inputObject['b'], inputObject['p'] = map(int, input[1].strip().split(' '))
    inputObject['m'], inputObject['n'] = map(int, input[2].strip().split(' '))
    return inputObject


def extEuclid(a, b):
    """
    calculates d, s, t such that d = gcd(a,b) and d == a*s + b*t
    Returns d, s and t.
    """
    # if b is 0, return a, 1 and 0
    if b == 0:
        return a, 1, 0
    # if b is not 0, calculate d, s and t
    else:
        d, s, t = extEuclid(b, a % b)
        return d, t, s - (a // b) * t

def posLam(lam, p):
    """
    Get positive lambda.
    Returns positive lambda.
    """
    # if lambda is negative, add p
    if lam < 0:
        lam += p
    return lam

def pointDoubling(P, a, p):
    """
    Double a point on the curve.
    P is the point to double.
    a is the parameter a of the curve.
    p is the parameter p of the curve.
    Returns the resulting point.
    """
    # calculate lambda
    lam = ((3 * P[0] ** 2 + a) * extEuclid(2 * P[1], p)[1]) % p
    # get positive lambda
    lam = posLam(lam, p)
    # calculate x
    x = (lam ** 2 - 2 * P[0]) % p
    # calculate y
    y = (lam * (P[0] - x) - P[1]) % p
    return [x, y]

def pointAddition(P, Q, a, p):
    """
    Add two points on the curve.
    P and Q are the points to add.
    a is the parameter a of the curve.
    p is the parameter p of the curve.
    Returns the resulting point.
    """
    # if P is the neutral element, return Q
    if P == [0, 0]:
        return Q
    # if Q is the neutral element, return P
    if Q == [0, 0]:
        return P
    # if P and Q are the same point, calculate point doubling
    if P == Q:
        return pointDoubling(P, a, p)
    # if P and Q are different points, calculate lambda
    lam = (Q[1] - P[1]) * extEuclid(Q[0] - P[0], p)[1] % p
    # get positive lambda
    lam = posLam(lam, p)
    # calculate x
    x = (lam ** 2 - P[0] - Q[0]) % p
    # calculate y
    y = (lam * (P[0] - x) - P[1]) % p
    return [x, y]

  
def pointMultiplication(P, n, a, p):
    """
    Multiply a point on the curve.
    P is the point to multiply.
    n is the number to multiply with.
    a is the parameter a of the curve.
    p is the parameter p of the curve.
    Returns the resulting point.
    """
    # if n is 1, return P
    if n == 1:
        return P
    # if n is even, calculate point doubling
    if n % 2 == 0:
        return pointMultiplication(pointDoubling(P, a, p), n // 2, a, p)
    # if y is 0 and n is odd, return P
    if P[1] == 0 and n % 2 == 1:
        return P
    # if n is odd, calculate point doubling and point addition
    else:
        return pointAddition(pointMultiplication(pointDoubling(P, a, p), (n - 1) // 2, a, p), P, a, p)


input = interpret_input(read_stdin())
# input = interpret_input(read_file('in/1.in.txt'))

# print shared key
print(tuple(pointMultiplication(input['coords'], input['m']*input['n'], input['a'], input['p'])))