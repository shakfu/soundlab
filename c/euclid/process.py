with open('euclid.txt') as f:
    result = []
    lines = f.readlines()
    lst = [line.strip() for line in lines]
    lst = [l.replace(':', ',') for l in lst]
    lst = [l.replace('E(', '') for l in lst]
    lst = [l.replace(')', '') for l in lst]
    lst = [l.split(',') for l in lst]
    for line in lst:
        try:
            for beats, length, pattern in lst:
                result.append((beats, length, pattern.strip()))
        except ValueError:
            continue

to_bin = lambda x: int(x,2)
to_hex = lambda x: hex(to_bin(x))

for b, l, p in result:
    print(b, l, to_bin(p))
