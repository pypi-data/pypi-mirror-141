import typing

_T = typing.TypeVar('_T')

class object:
    def __init__(self) -> None: pass

class type:
    def __init__(self, x: typing.Any) -> None: pass

class function: pass

property = object()  # Dummy definition

class dict: pass
class int: pass
class str: pass
class bytes: pass
class bool: pass
class ellipsis: pass

class tuple(typing.Generic[_T]): pass
