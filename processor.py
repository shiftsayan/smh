'''
Song Processor
Takes a .wav file and generates enemy timings based on beat drops and changes in the song
'''

# Imports

import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.io.wavfile import read
from random import randint
import json
import sobol # from FSU
import copy
import decimal

# Songs
JSONPATH = './json/'
SONGPATH = './music/'
SONGNAME = 'shapeofyou' # Change song name here

# Cleanup Utility

def cleanup(result):
    r_copy = copy.deepcopy(result)
    same = 1
    current = result[0][1]
    deleted = 0
    for item in result:
        if item[1] == current:
            if same > 4:
                r_copy.remove(item)
            else:
                same += 1
        else:
            same = 1
            current = item[1]
    return r_copy

# Math Functions

def roundCeiling(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_CEILING
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def mean(previous):
    s = 0
    n = 0
    for item in previous:
        if item != 0:
            s += item
            n += 1
    try: return s/n
    except ZeroDivisionError:
        return s

# Main Function

def main():
    fs, audio = read(SONGPATH + SONGNAME + '.wav')
    audio = audio[:,0]
    audio = audio.astype(np.int64)

    window_time = 0.33
    sensitivity = 1
    history = 40

    # Analysis
    ts = 1/fs
    windowSize = int(window_time/ts)
    audio = audio[0:audio.shape[0]-(audio.shape[0]%windowSize)]
    nWindows = int(audio.shape[0]/windowSize)
    windows = np.hsplit(audio, nWindows)
    count = -1
    result = []
    previous = []

    for window in windows:
        count += 1
        energy = np.sum(np.square(window))
        previous.append(energy)
        if len(previous) > history:
            previous.pop(0)
        avg_history = mean(previous)
        if energy * sensitivity > avg_history:
            if len(result) > 1 and count*window_time*1000 - result[-1][0] <= 300: # no overlapping circles
                continue
            result.append([roundHalfUp(count*window_time*1000)])

    sob = sobol.i4_sobol_generate(1, len(result), 5)
    no_change = 0

    for i in range(len(result)):
        if i > 1 and result[i][0] - result[i-1][0] < 660: # minimum time for possible switch
            result[i].append(result[i-1][1])
        else:
            k = roundCeiling(sob[0][i] * 3) - 1
            if k < 0:
                k = 0
            if i > 1 and result[i-1][1] == k:
                k += 1
            if k > 2:
                k = 0
            result[i].append(k)

    with open(JSONPATH + SONGNAME + '.json', 'w') as f:
        json.dump(result, f)

if __name__ == '__main__':
    main()
