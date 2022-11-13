# euclidean rhythms

- interesting article: [euclidean-rhythms](https://observablehq.com/@toja/euclidean-rhythms) with a javascript definition of the algorithm for `E(pulses, steps) -> rhythm` where `rhythm` is a string of 1s and 0s and also some historical context on the link to euclid's GCD(x,y) function of two numbers.

```javascript

function E(pulses, steps) {
	if (pulses > steps)
		pulses = steps;

 	// step 0
 	let a = "1";
 	let b = "0";
 	let k = pulses;
 	let m = steps - pulses;

 	let cpy, tmp;

	do {
		cpy = a;
    	a += b;
		if (k <= m) {  // step 1
      		m -= k;
		} else {       // step 2, 3
      		b = cpy;
      		tmp = k;
      		k = m;
			m = tmp - m;
		}
	} while (m > 1 & k > 1);

  	// step 4
	let rhythm = "";
	while (k > 0) (rhythm += a, --k);
	while (m > 0) (rhythm += b, --m);

	return rhythm;
}
```

A conversion to python:

```python
def euclid(pulses, steps):
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
```
