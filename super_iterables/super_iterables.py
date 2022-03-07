import abc
from functools import reduce
from itertools import groupby
from typing import Any, Callable, Generic, Iterable, Optional, Tuple, TypeVar, Union

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")


class superdict(dict, Generic[_K, _V]):
    def to_list(self) -> "superlist[Tuple[_K, _V]]":
        return superlist([(k, v) for k, v in self.items()])

    def to_set(self) -> "superset[Tuple[_K, _V]]":
        return superset(self.items())

    def map(self, func: Callable[[_K, _V], _T]) -> "superdict[_K, _T]":
        return superdict({k: func(k, v) for k, v in self.items()})

    def map_values(self, func: Callable[[_V], _T]) -> "superdict[_K, _T]":
        return superdict({k: func(v) for k, v in self.items()})

    def map_keys(self, func: Callable[[_K], _T]) -> "superdict[_T, _V]":
        return superdict({func(k): v for k, v in self.items()})

    def value_list(self) -> "superlist[_V]":
        return superlist(v for v in self.values())

    def key_list(self) -> "superlist[_K]":
        return superlist(k for k in self.keys())

    def value_set(self) -> "superset[_V]":
        return superset(self.values())

    def key_set(self) -> "superset[_K]":
        return superset(self.keys())

    def sorted_keys(self) -> "superlist[_K]":
        return superlist(sorted(self.keys()))

    def sorted_values(self) -> "superlist[_V]":
        return superlist(sorted(self.values()))

    def reverse(self) -> "superdict[_V, _K]":
        return superdict({v: k for k, v in self.items()})


class superlist(list, Generic[_T]):
    def copy(self: "superlist[_T]") -> "superlist[_T]":
        return superlist(self.copy())

    def extend(self, __iterable: Iterable[_T]) -> None:
        return super().extend(__iterable)

    def to_dict(self: "superlist[Tuple[_K, _V]]") -> "superdict[_K, _V]":
        return superdict(self)

    def map(self, f: Callable[[_T], _K]) -> "superlist[_K]":
        return superlist(map(f, self))

    def for_each(self, f: Callable[[_T], None]) -> None:
        for v in self:
            f(v)

    def filter(self, f: Callable[[_T], bool]) -> "superlist[_T]":
        return superlist(filter(f, self))

    def filter_not(self, f: Callable[[_T], bool]) -> "superlist[_T]":
        return superlist(filter(lambda x: not f(x), self))

    def reduce(self, f: Callable[[_T, _T], _T]) -> _T:
        return reduce(f, self)

    def partition(
        self, f: Callable[[_T], bool]
    ) -> Tuple["superlist[_T]", "superlist[_T]"]:
        return superlist(filter(f, self)), superlist(filter(lambda x: not f(x), self))

    def group_by(self, f: Callable[[_T], _K]) -> "superdict[_K, superlist[_T]]":
        return superdict([(k, superlist(v)) for k, v in groupby(self, f)])

    def to_set(self) -> "superset[_T]":
        return superset(self)

    def head(self) -> "_T":
        if len(self) > 0:
            return self[0]
        raise IndexError("Empty list")

    def head_option(self) -> "Option[_T]":
        if len(self) > 0:
            return Some(self[0])
        return NullOption()

    def find(self: "superlist[_T]", f: Callable[[_T], bool]) -> "Option[_T]":
        for v in self:
            if f(v):
                return Some(v)
        return NullOption()

    def flatten(self: "superlist[superlist[_T]]") -> "superlist[_T]":
        return superlist([v for sublist in self for v in sublist])

    def flat_map(
        self: "superlist[_T]", f: Callable[[_T], "superlist[_V]"]
    ) -> "superlist[_V]":
        return superlist([v for sublist in self for v in f(sublist)])

    def star_map(
        self: "superlist[_T]", f: Callable[[_T], "superlist[_V]"]
    ) -> "superlist[_V]":
        return superlist([f(*v) for v in self])

    def make_string(
        self,
        start: str = "",
        end: str = "",
        sep: str = "",
        func: Callable[[_T], str] = str,
    ) -> str:
        return start + sep.join(map(func, self)) + end

    def pluck(self: "superlist[dict[_K, _V]]", key: _K) -> "superlist[_V]":
        return superlist([v[key] for v in self])

    def sort_by(
        self: "superlist[_T]", f: Callable[[_T], Any], reverse: bool = False
    ) -> "superlist[_T]":
        return superlist(sorted(self, key=f, reverse=reverse))

    def sorted(
        self: "superlist[_T]",
        by: Optional[Callable[[_T], Any]] = None,
        reverse: bool = False,
    ) -> "superlist[_T]":
        return superlist(sorted(self, key=by, reverse=reverse))

    def __getslice__(self, i, j) -> "superlist[_T]":
        return superlist(self[i:j])

    def __add__(self, other: "superlist[_T]") -> "superlist[_T]":
        return superlist(list.__add__(self, other))

    def __iadd__(self, other: "superlist[_T]") -> "superlist[_T]":
        return superlist(list.__iadd__(self, other))

    def __mul__(self, other: int) -> "superlist[_T]":
        return superlist(list.__mul__(self, other))

    def __imul__(self, other: int) -> "superlist[_T]":
        return superlist(list.__imul__(self, other))

    def __rmul__(self, other: int) -> "superlist[_T]":
        return superlist(list.__rmul__(self, other))


class superset(set, Generic[_T]):
    def to_list(self) -> "superlist[_T]":
        return superlist(self)

    def map(self, f: Callable[[_T], _K]) -> "superset[_K]":
        return superset(map(f, self))

    def filter(self, f: Callable[[_T], bool]) -> "superset[_T]":
        return superset(filter(f, self))

    def filter_not(self, f: Callable[[_T], bool]) -> "superset[_T]":
        return superset(filter(lambda x: not f(x), self))

    def reduce(self, f: Callable[[_T, _T], _T]) -> _T:
        return reduce(f, self)

    def partition(
        self, f: Callable[[_T], bool]
    ) -> Tuple["superset[_T]", "superset[_T]"]:
        return superset(filter(f, self)), superset(filter(lambda x: not f(x), self))

    def group_by(self, f: Callable[[_T], _K]) -> "superdict[_K, superset[_T]]":
        return superdict([(k, superset(v)) for k, v in groupby(self, f)])

    def union(self, *s: Iterable[_K]) -> "superset[Union[_T, _K]]":
        return superset(super().union(*s))

    def intersection(self, *s: Iterable[_K]) -> "superset[Union[_T, _K]]":
        return superset(super().intersection(*s))

    def difference(self, *s: Iterable[_K]) -> "superset[Union[_T, _K]]":
        return superset(super().difference(*s))

    def symmetric_difference(self, *s: Iterable[_K]) -> "superset[Union[_T, _K]]":
        return superset(super().symmetric_difference(*s))

    def copy(self) -> "superset[_T]":
        return superset(self.copy())

    def sort_by(self, f: Callable[[_T], Any], reverse: bool = False) -> "superlist[_T]":
        return superlist(sorted(self, key=f, reverse=reverse))

    def sorted(
        self, by: Optional[Callable[[_T], Any]] = None, reverse: bool = False
    ) -> "superlist[_T]":
        return superlist(sorted(self, key=by, reverse=reverse))

    def for_each(self, f: Callable[[_T], None]) -> None:
        for v in self:
            f(v)


class Option(Generic[_T], abc.ABC):
    @abc.abstractmethod
    def __eq__(self, other):
        ...

    @abc.abstractmethod
    def __hash__(self):
        ...

    @abc.abstractmethod
    def __repr__(self):
        ...

    @abc.abstractmethod
    def __str__(self):
        ...

    @abc.abstractmethod
    def get(self) -> _T:
        ...

    @abc.abstractmethod
    def get_or_else(self, default: _T) -> _T:
        ...

    @abc.abstractmethod
    def is_defined(self) -> bool:
        ...

    @abc.abstractmethod
    def is_empty(self) -> bool:
        ...

    @abc.abstractmethod
    def map(self, f: Callable[[_T], _V]) -> "Option[_V]":
        ...

    @abc.abstractmethod
    def flat_map(self, f: Callable[[_T], "Option[_V]"]) -> "Option[_V]":
        ...

    @abc.abstractmethod
    def filter(self, f: Callable[[_T], bool]) -> "Option[_T]":
        ...

    @abc.abstractmethod
    def filter_not(self, f: Callable[[_T], bool]) -> "Option[_T]":
        ...

    @abc.abstractmethod
    def or_else(self, default: _T) -> _T:
        ...


class NullOption(Option):
    def __bool__(self) -> bool:
        return False

    def __eq__(self, other) -> bool:
        return isinstance(other, NullOption)

    def __hash__(self) -> int:
        return hash(None)

    def __repr__(self) -> str:
        return "NullOption"

    def __str__(self) -> str:
        return "NullOption"

    def get(self) -> None:
        raise ValueError("Option is empty")

    def get_or_else(self, default: _T) -> _T:
        return default

    def is_defined(self) -> bool:
        return False

    def is_empty(self) -> bool:
        return True

    def map(self, f: Callable) -> "NullOption":
        return NullOption()

    def flat_map(self, f: Callable) -> "NullOption":
        return NullOption()

    def filter(self, f: Callable) -> "NullOption":
        return NullOption()

    def filter_not(self, f: Callable) -> "NullOption":
        return NullOption()

    def or_else(self, default: _T) -> _T:
        return default


class Some(Generic[_T], Option[_T]):
    def __init__(self, value: _T):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Some) and self.value == other.value

    def __hash__(self):
        return hash(self.value)

    def __repr__(self):
        return f"Option({self.value})"

    def __str__(self):
        return f"Option({self.value})"

    def get(self) -> _T:
        return self.value

    def get_or_else(self, default: _T) -> _T:
        return self.value

    def is_defined(self) -> bool:
        return True

    def is_empty(self) -> bool:
        return False

    def map(self, f: Callable[[_T], _V]) -> "Option[_V]":
        return Some(f(self.value))

    def flat_map(self, f: Callable[[_T], "Option[_V]"]) -> "Option[_V]":
        return f(self.value)

    def filter(self, f: Callable[[_T], bool]) -> "Option[_T]":
        if f(self.value):
            return Some(self.value)
        else:
            return NullOption()

    def filter_not(self, f: Callable[[_T], bool]) -> "Option[_T]":
        if not f(self.value):
            return Some(self.value)
        else:
            return NullOption()

    def or_else(self, default: _T) -> _T:
        return self.value


test: superlist[int] = superlist([1, 2, 3])

# a = test.map(lambda x: x + 1).filter(lambda x: x > 2).map(lambda x: (x, x)).to_dict()

a: superlist[superdict[int, int]] = superlist(
    [superdict({1: 1, 2: 2, 3: 3}), superdict({1: 1, 2: 2, 3: 3})]
)

b = test.find(lambda x: x == 2).map(lambda x: x + 1).get_or_else(3)

# TODO
# - test with unit tests of other packages
