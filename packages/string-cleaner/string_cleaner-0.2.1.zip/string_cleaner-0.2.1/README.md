# String cleaner
Module for clean string from special chars and replace it by html-entity.

#### In current version (0.2.0):
* Replace special chars from string by html-entity based on the json entity map
    * symbol - "
    * symbol - '
    * symbol - >
    * symbol - <
    * another quote symbols
* Support possibility work with context manager.

#### In next versions:
* 0.3 — additional users rule for replace

#### How to use:
For first install module in your virtual environment:
```commandline
pip install string-cleaner
```
After this you can import this module and use it:
```python
from string_cleaner import cleaner
clean_string = cleaner.TakeString('<script>alert(123)</script>').make_clean_string()
```

Also you can use it with context manager:
```python
from string_cleaner import cleaner

with cleaner.TakeString('<test>') as clean_string:
    print(clean_string)
```
