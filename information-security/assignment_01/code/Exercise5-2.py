import sys

# # import input from 0.in.txt
# sys.stdin = open('0.in.txt', 'r')

# # interpret input
# input = sys.stdin.read().split()
# minKeySize = int(input[0])
# maxKeySize = int(input[1])
# ciphertext = ''.join(input[2:])
# likelyMostAccuringChar = 'e'

# # replace all non-alphabetic characters with dashes and convert to lowercase
# ciphertext = ''.join([c if c.isalpha() else '-' for c in ciphertext]).lower()


def std(vector):
    # caculate the standard deviation of a vector
    mean = sum(vector) / len(vector)
    return (sum([(v - mean) ** 2 for v in vector]) / len(vector)) ** 0.5


def getShift(char, likelyMostAccuringChar):
    # get the shift of a character to the most frequent character
    return ord(char) - ord(likelyMostAccuringChar)


def getLikelyKey(freqVectors, likelyMostAccuringChar):
    # get the shift of each character to the most frequent character
    shifts = [getShift(chr(vector.index(max(vector)) + ord('a')),
                       likelyMostAccuringChar) for vector in freqVectors]
    # get the key from the key shifts
    return ''.join([chr((shift + 26) % 26 + ord('a')) for shift in shifts])


def calcByKeySize(keySize, ciphertext):
    # split ciphertext into blocks of keySize
    blocks = [[*ciphertext[i:i + keySize]]
              for i in range(0, len(ciphertext), keySize)]
    # fill remaining block with dashes
    blocks[-1] += ['-'] * (keySize - len(blocks[-1]))
    # rotate blocks to get keySize coloumns (vectors)
    columns = list(zip(*blocks))
    # convert every column to a frequency vector
    freqVectors = [
        [column.count(c) for c in 'abcdefghijklmnopqrstuvwxyz'] for column in columns
    ]
    # compute the standard deviation of each vector
    stds = [std(vector) for vector in freqVectors]
    # sum of standard deviations
    return {'stdSum': sum(stds), 'freqVecs': freqVectors}


def printCipherBreakResults(ciphertext, minKeySize, maxKeySize, likelyMostAccuringChar):
    # keep track of highest std sum
    highestSTDSum = 0
    # list to store the frequency vectors of the key length with the highest sum of standard deviations
    bestFreqVectors = None
    for keySize in range(minKeySize, maxKeySize + 1):
        guess = calcByKeySize(keySize, ciphertext)
        # check if the sum of standard deviations is higher than the highest sum of standard deviations
        if guess['stdSum'] > highestSTDSum:
            # update the highest sum of standard deviations
            highestSTDSum = guess['stdSum']
            # update the best frequency vectors
            bestFreqVectors = guess['freqVecs']
        # sum the standard deviations and print
        print('The sum of {} std. devs: {:.2f}'.format(
            keySize, guess['stdSum']))
    # print the key guess
    printKeyGuess(bestFreqVectors, likelyMostAccuringChar)


def printKeyGuess(bestFreqVectors, likelyMostAccuringChar):
    # get the likely key
    likelyKey = getLikelyKey(bestFreqVectors, likelyMostAccuringChar)
    # print the key guess
    print('\nKey guess:\n{}'.format(likelyKey))


def handle_input(input):
    if len(input) >= 3:
        printCipherBreakResults(
            ''.join(
                [c if c.isalpha() else '' for c in input[2]]
            ).lower(),
            int(input[0]),
            int(input[1]),
            'e'
        )
    else:
        print("Invalid input")


def main():
    totalInput = []
    # get input text
    for line in sys.stdin:
        if line.strip() == '':
            break
        totalInput.append(line)
    handle_input([totalInput[0], totalInput[1], ''.join(totalInput[2:])])


if __name__ == "__main__":
    main()
