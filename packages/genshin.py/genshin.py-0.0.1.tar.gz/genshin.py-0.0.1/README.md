# Genshin.py

A simple wrapper for the genshin api for python

### Installation:
`pip install genshin.py`


### Usage:
```python
import genshin

g = genshin.Genshin(local=False)

c = g.api("characters")
print(c.values)
print(g.types)
print()
```