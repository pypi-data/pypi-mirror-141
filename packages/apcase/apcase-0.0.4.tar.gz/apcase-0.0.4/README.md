### sample

code：
```python
from apcase import ap

data = [
    [1, 2, 3],
    [4, 5, 6]
]

print(ap.allpairs(data))
```

result:
```text
[(1, 4), (1, 5), (1, 6), (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6)]
```

code:
```python
from apcase import ap

data = [
    [1, 2, 3],
    [4, 5, 6]
]

for a, b in ap.allpairs(data):
    print("a=%s&b=%s" % (a, b))
```

result:
```text
a=1&b=4
a=1&b=5
a=1&b=6
a=2&b=4
a=2&b=5
a=2&b=6
a=3&b=4
a=3&b=5
a=3&b=6
```