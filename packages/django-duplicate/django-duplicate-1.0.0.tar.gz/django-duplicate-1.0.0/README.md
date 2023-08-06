Django Duplicate
========

![example workflow](https://github.com/innovationinit/django-duplicate/actions/workflows/test-package.yml/badge.svg?branch=main)
[![Coverage Status](https://coveralls.io/repos/github/innovationinit/django-duplicate/badge.svg)](https://coveralls.io/github/innovationinit/django-duplicate)


Django-Duplicate has an util tool for making a deep copy of django model instances

duplicate.utils.duplicate
-------------------------
Creates and returns a  new object that is identical to ``instance``.


DuplicateMixin
--------------
Mixin for model classes which implements duplicate function as method.

```python
from django.db import models

from duplicate.models import DuplicateMixin


class Book(DuplicateMixin, models.Model):
    title = models.CharField(max_lenght=100)
    author = models.ForegnKey('library.Author')
```

Let's duplicate (shallow copy) book instance:

```python
book = Book(title='Two Scoops of Django')
boook.save()

book_copy = book.duplicate()
```

If you wanna do deep (related models gonna be shallow copied) copy use `paths` argument of duplicate method. `paths` should be list of relation paths:

```python
book_copy = book.duplicate(paths=['author'])
```

To shallow copy every relation on some level use `*` symbol:

```python
book_copy = book.duplicate(paths=['*'])
```

`author.*` path would copy also all author relations.

There is also symbol `~` which means "reference relations, but if reference object is duplicated in the context use it instead".


You can override fields like this(You cannot override nested m2m fields): 
```python

book_copy = book.duplicate(paths=['author'], override_fields={'author.name': 'Overriden author name'})


from duplicate.utils import CallableValue
book_copy = book.duplicate(paths=['author'], override_fields={'author.name': 'Overriden author name'})

```

You can also override nested fields with callable that takes instace on which you are overriding field as an argument:
```python
from duplicate.utils import CallableValue

book_copy = book.duplicate(
    paths=['author'],
    override_fields={
        'author.name': CallableValue(lambda author: 'Professional author name' if author.professional else 'Author name')
    }
)

```

DJANGO_DUPLICATE_KNOWN_RELATIONS
--------------------------------

To ensure that code is aware of all possible to duplicate models and relations path project should have setting `DJANGO_DUPLICATE_KNOWN_RELATIONS` which is a dict with model labels as keys and list of model relations as value:

```python
DJANGO_DUPLICATE_KNOWN_RELATIONS = {
    "duplicate.Author": [
        "book_set",
    ],
    "duplicate.Book": [
        "author",
    ],
}
```

This app enables check which will throw errors when state of app will not correspond to value of `DJANGO_DUPLICATE_KNOWN_RELATIONS`.

## License
The Django Wicked Historian package is licensed under the [FreeBSD
License](https://opensource.org/licenses/BSD-2-Clause).
