# Implement Diffie-Hellman key exchange featuring Elliptical Curve Cryptography
import sys

def calculate_part(p, g, a):
    return pow(g, a, p)

def calculate_key(p, g, a, b):
    return pow(g, a * b, p)


def read_file(filename):
    with open(filename, 'r') as f:
        return f.readlines()

def read_stdin():
    return sys.stdin.readlines()

def main():

    # read file
    input = read_file('in/0.in.txt')
    ouput = read_file('out/0.out.txt')

    print(input)
    print(ouput)

    # read input

    # print("p =", p)
    # print("g =", g)
    # print("a =", a)
    # print("b =", b)

    # print("A calculates key:", calculate_key(p, g, a, b))
    # print("B calculates key:", calculate_key(p, g, b, a))

    # print("A calculates part:", calculate_part(p, g, a))
    # print("B calculates part:", calculate_part(p, g, b))
    # print("A calculates key:", calculate_part(p, calculate_part(p, g, b), a))
    # print("B calculates key:", calculate_part(p, calculate_part(p, g, a), b))

if __name__ == "__main__":
    main()