# knapsack key validation

import sys

def split_key_string(key):
    key_list = key.split()
    for i in range(len(key_list)):
        key_list[i] = int(key_list[i])
    return key_list

def validate_key(key, n):
    key_sum = 0
    for i in range(len(key)):
        if key[i] <= key_sum:
            return False
        key_sum += int(key[i])
    if key_sum > n:
        return False
    return True

def make_public_key(private_key, m, n):
    public_key_generated = []
    for i in range(len(private_key)):
        public_key_generated.append((private_key[i] * m) % n)
    return public_key_generated


def validate_knapsack(m, n, private_key, public_key):
    if len(private_key) != len(public_key):
        return 0
    if n <= 0 or m <= 0 or n % m == 0:
        return -1
    if not validate_key(private_key, n):
        return -1
    if make_public_key(private_key, m, n) != public_key:
        return 0
    return 1

def main():
    m, n = sys.stdin.buffer.readline().split()

    n = int(n)
    m = int(m)

    private_key = split_key_string(sys.stdin.buffer.readline())
    public_key = split_key_string(sys.stdin.buffer.readline())
    print(validate_knapsack(m, n, private_key, public_key))

if __name__ == '__main__':
    main()