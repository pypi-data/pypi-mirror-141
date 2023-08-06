[![](https://img.shields.io/pypi/v/dictat.svg?maxAge=3600)](https://pypi.org/project/dictat/)
[![Latest Release](https://gitlab.com/janoskut/dictat/-/badges/release.svg)](https://gitlab.com/janoskut/dictat/-/releases)
[![pipeline status](https://gitlab.com/janoskut/dictat/badges/main/pipeline.svg)](https://gitlab.com/janoskut/dictat/-/commits/main)
[![coverage report](https://gitlab.com/janoskut/dictat/badges/main/coverage.svg)](https://gitlab.com/janoskut/dictat/-/commits/main)
[![](https://img.shields.io/badge/License-Unlicense-blue.svg?longCache=True)](https://unlicense.org/)
[![](https://img.shields.io/badge/dependencies-none-informational)]()

`Adict` is an attribute-accessible dynamic dict wrapper, which allows to access dict items in
attribute notation (".") and allows friendly checks for non-existing items.

`Adict` is not an _extension_ of Python's `dict` (as for example
[adict](https://test.pypi.org/project/adict/) and [dict](https://test.pypi.org/project/dict/)),
but a _wrapper_ around `dict` objects. This allows to use attribute syntax not only for objects
created using the `Adict()` constructor, but also for child dictionaries, which are automatically
wrapped into an `Adict` when they're returned.

# Features

- Default `dict` behavior
- Full wrapping of nested `dict`s
- Fail-safe attribute notation (`adict.key`) doesn't raise `KeyError`
- Supports nested dicts
- Supports JSON encoding


# Installation

```sh
pip install dictat
```


# Examples

```py
from dictat import Adict

dict1 = Adict()
print('noob' in dict1)          # False
print(dict1.noob)               # None - doesn't fail
# print(dict1['noob'])          # raises KeyError - default dict behavior
dict1.noob = 'me'
print(dict1['noob'])            # "me" - dict notation
print(dict1.noob)               # "me" -, attribute notation
dict1.sub = {}
dict1.sub.dict = {'noobs': ['me', 'you']}
print(dict1.sub.dict.noobs[1])  # "you"

dict2 = {'noob': 'me', 'sub': {'you': 'noob'}}
dict3 = Adict(dict2)            # construct around existing dict
print('noob' in dict3)          # True
print(dict3['noob'])            # "me", dict notation
print(dict3.noob)               # "me", attribute notation
print(dict3.sub.you)            # "noob', nested attribute notation
```

## JSON encoding

```py
from dictat import Adict, JsonEncoder

import json
import pathlib

adict = Adict()
adict.key = 'string'
adict.sub = dict(subkey='subvalue', obj=object())
adict.path = pathlib.Path('somepath')  # normally not JSON serializable

dump = json.dumps(adict, cls=JsonEncoder)
print(dump)

# {"key": "string", "sub": {"subkey": "subvalue"}, "path": "somepath"}
```
