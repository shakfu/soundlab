def euclid(n: int, hits: int, offset: int = 0, length: int = 16):
    for i in range(n):
        s1 = i + offset
        s2 = s1 * hits
        s3 = s2 % length
        s4 = int(s3 < hits)
        yield s4
