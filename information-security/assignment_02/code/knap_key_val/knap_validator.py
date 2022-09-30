# knapsack key validation

import sys

def split_key_string(key):
    key_list = key.split()
    for i in range(len(key_list)):
        key_list[i] = int(key_list[i])
    return key_list

def validate_key(key):
    key_sum = 0
    for i in range(len(key)):
        if int(key[i]) < key_sum:
            return False
        key_sum += int(key[i])
    return True

def make_public_key(private_key, m, n):
    public_key_generated = []
    for i in range(len(private_key)):
        public_key_generated.append((int(private_key[i]) * n) % m)
    return public_key_generated


def validate_knapsack(m, n, private_key, public_key):
    if not validate_key(private_key):
        return -1
    if make_public_key(private_key, m, n) != public_key:
        return 0
    return 1

def main():
    n, m = sys.stdin.buffer.readline().split()

    n = int(n)
    m = int(m)

    private_key = split_key_string(sys.stdin.buffer.readline())
    public_key = split_key_string(sys.stdin.buffer.readline())
    print(validate_knapsack(m, n, private_key, public_key))

    # n = 41 
    # m = 491
    # private_key = split_key_string("2 3 7 14 30 57 120 233")
    # public_key = split_key_string("82 123 287 83 248 373 10 471")
    # print(validate_knapsack(m, n, private_key, public_key))

if __name__ == '__main__':
    main()