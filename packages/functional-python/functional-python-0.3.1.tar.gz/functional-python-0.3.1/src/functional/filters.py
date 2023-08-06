"""
A group of helper classes implementing filters.
Filters are function-like classes those can, well,
filter the given sequence for the given conditions.

The main difference between them and normal functions or lambdas
is the fact all classes in this file are frozen dataclasses and support hashing.
"""
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import *

__pdoc__ = dict()

T = TypeVar('T')
FilterLikeCallable = Callable[[T], bool]

if (sys.version_info >= (3, 8)):
    class FilterLike(FilterLikeCallable, Protocol, Generic[T]):
        """ A `typing.Protocol` implementation of `Callable[[T], bool]` """
        def __call__(self, el: T) -> bool:
            pass

else:
    class FilterLike(FilterLikeCallable, Generic[T]):
        """ A Protocol-like implementation of `Callable[[T], bool]` used for Python < 3.8 """
        def __call__(self, el: T) -> bool:
            pass


@dataclass(frozen=True)
class AbstractFilter(Generic[T], FilterLikeCallable, ABC):
    """
    A parent class for filters.
    Implements the core logic (yes) of filtering by calling the built-in `builtins.filter`
    which is a bit faster than lambdas or generator expressions.
    
    When inheriting from this class, make sure:
     * `check_element` method is implemented
     * Class is marked with `dataclass(frozen=True)` decoration
    
    Basically, all filter classes are same as the following:
    ```python
    filtered = filter(lambda el: my_func(el, param1, param2), seq)
    filtered = MyFilter(param1, param2).filter(seq)
    filtered = filter(MyFilter(param1, param2), seq)
    ```
    
    Usage:
        ```python
        @dataclass(frozen=True)
        class GEFilter(AbstractFilter[int]):
            than: int
            
            def check_element(self, el: int) -> bool:
                return el >= self.than
        
        lst = [ -1, 3, 8, 5, 0, -6, 7 ]
        for el in GEFilter(5).filter(lst):
            print(el)
        # Output:
        # 8 5 7
        ```
    """
    
    @abstractmethod
    def check_element(self, el: T) -> bool:
        """
        An abstract method that implements per-element filtering.
        Returns `True` if the given element matches condition.
        
        Args:
            el: `T`
            An element to check.
        
        Returns:
            `bool`.
        """
        pass
    
    def filter(self, seq: Iterable[T]) -> Iterator[T]:
        """
        Filters the given sequence via itself.
        
        Args:
            seq: `Iterable[T]`.
                A sequence to filter.
        
        Returns:
            `Iterator[T]`.
                A filtered sequence.
        """
        
        # noinspection PyArgumentList
        return filter(self.check_element, seq)
    
    @overload
    def __call__(self, el: T) -> bool:
        """
        Same as `AbstractFilter.check_element()`
        
        See Also:
            * `AbstractFilter.check_element()`
        """
        pass
    def __call__(self, *args, **kwargs) -> bool:
        return self.check_element(*args, **kwargs)


@dataclass(frozen=True)
class HasAttrFilter(AbstractFilter, Generic[T]):
    """
    An `AbstractFilter` implementation of Python `lambda el: hasattr(el, attr_name)`.
    Filters all elements those have the given attribute.
    """
    
    attr_name: str
    """ An attribute name to check. """
    
    def check_element(self, el: T) -> bool:
        return hasattr(el, self.attr_name)

@dataclass(frozen=True)
class _IsNotNoneFilter(AbstractFilter[Optional[T]], Generic[T]):
    """
    An `AbstractFilter` implementation of Python `lambda el: el is not None`.
    Filters-out all None elements.
    
    This class is a singleton.
    """
    
    def check_element(self, el: Optional[T]) -> bool:
        return el is not None
    
    def filter(self, seq: Iterable[Optional[T]]) -> Iterator[T]:
        pass

@dataclass(frozen=True)
class AndFilter(AbstractFilter[T], Generic[T]):
    """
    An `AbstractFilter` implementation of Python `lambda el: all(f(el) for f in filters)`.
    Simple logical filter that returns True only if an element matches all its sub-filters.
    
    Note that:
     * The sequence of filters is lazy-applied.
     * `AndFilter` of an empty sequence is `True`
    """
    
    filters: Iterable[FilterLike[T]]
    """ A sequence of filters to apply. """
    
    def check_element(self, el: T) -> bool:
        return all(f(el) for f in self.filters)

@dataclass(frozen=True)
class OrFilter(AbstractFilter[T], Generic[T]):
    """
    An `AbstractFilter` implementation of Python `lambda el: any(f(el) for f in filters)`.
    Simple logical filter that returns True if an element matches any of its sub-filters.
    
    Note that:
     * The sequence of filters is lazy-applied.
     * `OrFilter` of an empty sequence is `False`
    """
    
    filters: Iterable[FilterLike[T]]
    """ A sequence of filters to apply. """
    
    def check_element(self, el: T) -> bool:
        return any(f(el) for f in self.filters)

@dataclass(frozen=True)
class NotFilter(AbstractFilter[T], Generic[T]):
    """
    An `AbstractFilter` implementation of Python `lambda el: not filter(el)`.
    Simple logical filter that inverts the result of the given filter.
    """
    
    filter: FilterLike[T]
    """ A filter instance to invert. """
    
    def check_element(self, el: T) -> bool:
        return not self.filter(el)


_IsNotNoneFilter.filter = AbstractFilter.filter
IsNotNoneFilter = _IsNotNoneFilter()
"""
An `AbstractFilter` implementation of Python `lambda el: el is not None`.
Filters-out all None elements.
"""


__all__ = \
[
    'AbstractFilter',
    'AndFilter',
    'FilterLike',
    'HasAttrFilter',
    'IsNotNoneFilter',
    'NotFilter',
    'OrFilter',
]
__pdoc__['_IsNotNoneFilter'] = True
__pdoc__['IsNotNoneFilter'] = True
