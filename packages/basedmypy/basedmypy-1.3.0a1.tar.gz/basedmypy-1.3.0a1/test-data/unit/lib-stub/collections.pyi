from typing import Any, Iterable, Union, Optional, Dict, TypeVar, overload, Optional, Callable, Sized

def namedtuple(
    typename: str,
    field_names: Union[str, Iterable[str]],
    *,
    # really bool but many tests don't have bool available
    rename: int = ...,
    module: Optional[str] = ...,
    defaults: Optional[Iterable[Any]] = ...
) -> Any: ...

KT = TypeVar('KT')
VT = TypeVar('VT')

class OrderedDict(Dict[KT, VT]): ...

class defaultdict(Dict[KT, VT]):
    def __init__(self, default_factory: Optional[Callable[[], VT]]) -> None: ...

class Counter(Dict[KT, int], Generic[KT]): ...

class deque(Sized, Iterable[KT], Reversible[KT], Generic[KT]): ...

class ChainMap(MutableMapping[KT, VT], Generic[KT, VT]): ...
