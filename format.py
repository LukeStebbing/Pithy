"""
Format a string using names in the current scope.


ScopeFormatter allows Python's string formatting to be used with names
drawn from the current scope, similar to the variable interpolation
found in languages such as Ruby and Perl.


.. contents::


Examples
--------
>>> from scopeformatter import F
>>> greeting = 'Hello'
>>> def greet(name):
...     return F('{greeting}, {name}!')
>>> greet('world')
'Hello, world!'

Positional and keyword arguments are accepted:

>>> F('{greeting} {0} times, {name}!', len(greeting), name='world')
'Hello 5 times, world!'


Requirements
------------
The stack inspection requires a Python VM that provides
``sys._getframe()``, such as CPython.


Limitations
-----------
Non-global names from enclosing scopes will not be found unless
they are referenced in the local scope.

>>> def outer():
...     non_local = 'non-local'
...     def inner():
...         return F('{non_local} is not referenced locally')
...     return inner()
>>> outer()
Traceback (most recent call last):
    ...
KeyError: 'non_local'

>>> def outer():
...     non_local = 'non-local'
...     def inner():
...         non_local
...         return F('{non_local} is referenced locally')
...     return inner()
>>> outer()
'non-local is referenced locally'

"""

from sys import _getframe

def F(*args, **kwds):
    """
    Format a string using names in the caller's scope.

    Names are looked up in the keyword arguments, then in the caller's
    locals, and finally in the caller's globals.

    Raises `KeyError` if a name is not found.

    """
    if not args:
        raise TypeError('F() takes at least 1 argument (0 given)')
    caller = _getframe(1)
    names = {}
    names.update(caller.f_globals)
    names.update(caller.f_locals)
    names.update(kwds)
    return args[0].format(*args[1:], **names)
