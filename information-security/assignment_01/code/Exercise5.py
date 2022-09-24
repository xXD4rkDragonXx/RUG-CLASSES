import re
import sys
import numpy as np

def textToKeyMatrix(text, keySize):
    # transform EncText to ndarray with shape (n, keySize)
    return np.array(list(text)[:len(text)-len(text) % keySize]).reshape(int(len(text)/keySize), keySize)


def replaceNonAlphaChars(text):
    # replace non alpha chars with dash
    return re.sub(r'[^a-zA-Z]', '-', text)


def occurencePerColumn(matrix):
    # calculate occurrences of each alphabetic character per column
    totalOccurences = []
    for i in range(matrix.shape[1]):
        occurences = np.unique(matrix[:, i], return_counts=True)
        # remove dashes from occurences if present
        if '-' in occurences[0]:
            occurences = (np.delete(occurences[0], np.where(
                occurences[0] == '-')), np.delete(occurences[1], np.where(occurences[0] == '-')))
        totalOccurences.append(occurences)
    return totalOccurences


def getMostFreqCharPerColumn(occurencePerColumn):
    # get most frequent character per column
    return [occurencePerColumn[i][0][np.argmax(occurencePerColumn[i][1])] for i in range(len(occurencePerColumn))]


def stdTotalSum(occurrences):
    # calculate the standard deviation of each column
    stds = np.array([np.std([int(count) for count in occurrences[i][1]])
                    for i in range(len(occurrences))])

    # return sum of max occurrences
    return np.sum(stds)


def getKeyShifts(mostFreqChars, mostFreqChar='e'):
    # get the shift of each character to the most frequent character
    return [ord(mostFreqChars[i]) - ord(mostFreqChar) for i in range(len(mostFreqChars))]


def keyShiftsToKey(keyShifts):
    # get the key from the key shifts
    return ''.join([chr((keyShifts[i] + 26) % 26 + ord('a')) for i in range(len(keyShifts))])


def printResultOf(input):
    minKeySize = int(input[0])
    maxKeySize = int(input[1])
    highestSTDSum = 0
    bestCharFreq = None
    # iterate over all possible key sizes
    for ks in range(minKeySize, maxKeySize + 1):
        charFreq = occurencePerColumn(
            textToKeyMatrix(replaceNonAlphaChars(input[2]), ks))
        totalSTDSum = stdTotalSum(charFreq)
        # keep track of the highest std sum
        if totalSTDSum > highestSTDSum:
            highestSTDSum = totalSTDSum
            bestCharFreq = charFreq
        print("The sum of %d std. devs: %s" %
              (ks, "{:.2f}".format(totalSTDSum)))

    print("Key guess:")
    print(keyShiftsToKey(getKeyShifts(getMostFreqCharPerColumn(bestCharFreq), 'e')))


def handle_input(input):
    if len(input) >= 3:
        printResultOf(input)
    else:
        print("Invalid input")


def main():
    totalInput = []
    # get input text
    for line in sys.stdin:
        if line == '\n':
            break
        totalInput.append(line.strip())
    handle_input([totalInput[0], totalInput[1], ''.join(totalInput[2:])])


if __name__ == "__main__":
    main()
