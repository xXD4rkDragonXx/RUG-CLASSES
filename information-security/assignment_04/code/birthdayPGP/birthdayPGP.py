import numpy as np
import gmpy2 as gmp
import time

def birthdayPGP(t, p):
    """
    Calculates the probability of a collision when p fingerprints are generated
    and t is the number of bits in the fingerprint.

    `t` is the number of bits in the fingerprint.
    `p` is the number of fingerprints generated.
    """
    # set time variable to track how long the function takes to run
    start = time.time()
    # calculate the amount of possible fingerprints
    t = 2 ** t + 1
    # t = 365 + 1
    # calculate print interval
    print_interval = int(p / 1000) if p > 1000 else 1
    # calculate the probability of a collision using product
    prob = 1
    for i in range(1, p):
        # calculate current probability using gmpy2
        prob = gmp.mul(prob, gmp.div(t - i, t))
        # prob = np.divide(np.multiply(prob, t - i), t)
        if i % print_interval == 0:
            # print prob in scientific notation
            print("Time elapsed: {:.2f} seconds, Progress: {}%".format(time.time() - start, i / print_interval / 10))
            # print expected remaining time
            print("Expected remaining time: {:.2f} seconds".format((time.time() - start) / i * (p - i)))
    # print the probability of a collision
    print("Probability of a collision: {:e}".format(1 - prob))

def main():
    # test the birthdayPGP function
    birthdayPGP(160, 7500000000)
    # birthdayPGP(160, 23)

if __name__ == "__main__":
    main()
    