"""euclidean: generate euclidean beats in python

The first is basically a literal translation of the swift function in
https://medium.com/code-music-noise/euclidean-rhythms-391d879494df

The second comes from https://kountanis.com/2017/06/13/python-euclidean/
for comparison.


"""

import math


def euclid(onsets, pulses):
    """returns a list of ones and zeros for a given euclidean rhythm

    >>> euclid(3,8)
    [1, 0, 0, 1, 0, 0, 1, 0]
    """
    slope = float(onsets) / float(pulses)
    result = []
    previous = None
    for i in range(pulses):
        current = int(math.floor(float(i) * slope))
        result.append(int(current != previous if 1 else 0))
        previous = current
    return result

E=euclid

def euclid_str(pulses, steps):
    """returns a string of ones and zeros for a given euclidean rhythm
    
    >>> euclid_str(3, 8)
    '10010010'

    """
    if (pulses > steps):
        pulses = steps
    a = "1"
    b = "0"
    k = pulses
    m = steps - pulses
    while (m > 1 and k > 1):
        cpy = a
        a += b
        if k <= m:
            m -= k
        else:
            b = cpy
            tmp = k
            k = m
            m = tmp - m
    rhythm = ""
    while (k > 0):
        rhythm += a
        k -= 1
    while (m > 0):
        rhythm += b
        m -= 1
    return rhythm



def realign(lst):
    "make the first entry of the list a beat"
    while lst[0] == 0:
        last = lst.pop()
        lst.insert(0, last)
    return lst


def euclid_ceil(onsets, pulses):
    """returns a list of ones and zeros for a give euclidean rhythm
    
    Uses the ceiling function instead of floor, but not so interesting
    because it begins on a rest, use the realign function to fix this.

    >>> euclid_ceil(3,8)
    [0, 1, 0, 1, 0, 0, 1, 0]
    """
    slope = float(onsets) / float(pulses)
    result = []
    previous = 0
    for i in range(pulses):
        current = int(math.ceil(float(i) * slope))
        result.append(int(current != previous if 1 else 0))
        previous = current
    return realign(result)


def euclidean_rhythm(beats, pulses):
    """Computes Euclidean rhythm of beats/pulses

    From: https://kountanis.com/2017/06/13/python-euclidean/
    Examples:
        euclidean_rhythm(8, 5) -> [1, 0, 1, 0, 1, 0, 1, 1]
        euclidean_rhythm(7, 3) -> [1, 0, 0, 1, 0, 1, 0]

    Args:
        beats  (int): Beats of the rhythm
        pulses (int): Pulses to distribute. Should be <= beats

    Returns:
        list: 1s are pulses, zeros rests
    """
    if pulses is None or pulses < 0:
        pulses = 0
    if beats is None or beats < 0:
        beats = 0
    if pulses > beats:
        beats, pulses = pulses, beats
    if beats == 0:
        return []

    rests = beats - pulses
    result = [1] * pulses
    pivot = 1
    interval = 2
    while rests > 0:
        if pivot > len(result):
            pivot = 1
            interval += 1
        result.insert(pivot, 0)
        pivot += interval
        rests -= 1

    return result
