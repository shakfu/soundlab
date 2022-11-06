"""euclidean: generate euclidean beats in python

The first is basically a literal translation of the swift function in
https://medium.com/code-music-noise/euclidean-rhythms-391d879494df

The second comes from https://kountanis.com/2017/06/13/python-euclidean/
for comparison.


"""

import math


def euclid0(n: int, hits: int, offset: int = 0, length: int = 16):
    """n and length are different (n is a counter)

    euclidean patterns recurs
    """
    for i in range(n):
        s1 = i + offset
        s2 = s1 * hits
        s3 = s2 % length
        s4 = int(s3 < hits)
        yield s4


def euclid1(hits: int, length: int = 16, offset: int = 0):
    """n <==> length as generator
    """
    for i in range(length):
        s1 = i + offset
        s2 = s1 * hits
        s3 = s2 % length
        s4 = int(s3 < hits)
        yield s4

def euclid1a(hits: int, length: int = 16, offset: int = 0):
    """n <==> length as generator
    """
    res = []
    for i in range(length):
        s1 = i + offset
        s2 = s1 * hits
        s3 = s2 % length
        s4 = int(s3 < hits)
        res.append(s4)
    return res

def euclid1b(hits: int, length: int = 16, offset: int = 0):
    """one-liner (-:
    """
    return [int((((i + offset) * hits) % length) < hits) for i in range(length)]


def euclid2(onsets, pulses):
    """returns a list of ones and zeros for a give euclidean rhythm

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

E=euclid2


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
