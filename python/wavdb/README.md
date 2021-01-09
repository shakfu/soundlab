# wav - sample splitting and mgmt



To delete files between min/max sizes. For example,



delete all .wav files with a size between 1M and 3M
```
find . -type f -name '*.wav' -size +1M  -size -3M -delete -print
```


