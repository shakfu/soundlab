
def euclid(pulses, steps):
    if (pulses > steps):
        pulses = steps
    a = "1"
    b = "0"
    k = pulses
    m = steps - pulses
    cpy = None
    tmp = None
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
    rhythm = []
    while (k > 0):
        rhythm.append(a)
        k -= 1
    while (m > 0):
        rhythm.append(b)
        m -= 1
    return ''.join(rhythm)

print(euclid(3, 7))
