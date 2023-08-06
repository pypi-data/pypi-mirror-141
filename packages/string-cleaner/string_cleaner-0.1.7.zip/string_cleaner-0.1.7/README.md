# String cleaner
Module for clean string from special chars and replace it by html-entity.

#### In current version (0.1.7):
* Replace special chars from string by html-entity based on the json entity map
    * symbol - "
    * symbol - '
    * symbol - >
    * symbol - <
    * another quote symbols

#### In next versions:
* 0.2 — possibility work with context manager
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
