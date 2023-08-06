import functools
from typing import Callable, List, Any, Optional, Union, Tuple

from .utils import get_function_positional_arguments_count


def map_method(self: List, function: Callable) -> List:
    mapping_function_arguments_count = get_function_positional_arguments_count(function)

    if mapping_function_arguments_count == 0 or mapping_function_arguments_count > 3:
        raise ValueError("Invalid number of positional arguments in the mapping function")

    if mapping_function_arguments_count == 1:
        return list(map(function, self))
    elif mapping_function_arguments_count == 2:
        return list(map(function, self, range(len(self))))
    elif mapping_function_arguments_count == 3:
        return [function(el, i, self) for i, el in enumerate(self)]


def filter_method(self: List, function: Callable) -> List:
    filter_function_arguments_count = get_function_positional_arguments_count(function)

    if filter_function_arguments_count == 0 or filter_function_arguments_count > 3:
        raise ValueError("Invalid number of positional arguments in the filter function")

    if filter_function_arguments_count == 1:
        return list(filter(function, self))
    elif filter_function_arguments_count == 2:
        return [el for i, el in enumerate(self) if function(el, i)]
    elif filter_function_arguments_count == 3:
        return [el for i, el in enumerate(self) if function(el, i, self)]


def foreach_method(self: List, function: Callable) -> None:
    foreach_function_arguments_count = get_function_positional_arguments_count(function)

    if foreach_function_arguments_count == 0 or foreach_function_arguments_count > 3:
        raise ValueError("Invalid number of positional arguments in the foreach function")

    if foreach_function_arguments_count == 1:
        for element in self:
            function(element)
    elif foreach_function_arguments_count == 2:
        for index, element in enumerate(self):
            function(element, index)
    elif foreach_function_arguments_count == 3:
        for index, element in enumerate(self):
            function(element, index, self)

    return None


def find_method(self: List, function: Callable) -> Any:
    find_function_arguments_count = get_function_positional_arguments_count(function)

    if find_function_arguments_count == 0 or find_function_arguments_count > 3:
        raise ValueError("Invalid number of positional arguments in the 'find' function. The passed callback function"
                         " can have three positional arguments: the current element of the array, the index of the"
                         " current element, and the entire array.")

    if find_function_arguments_count == 1:
        for element in self:
            if function(element):
                return element

    elif find_function_arguments_count == 2:
        for index, element in enumerate(self):
            if function(element, index):
                return element

    elif find_function_arguments_count == 3:
        for index, element in enumerate(self):
            if function(element, index, self):
                return element

    return None


def find_index_method(self: List, function: Callable) -> int:
    find_index_function_arguments_count = get_function_positional_arguments_count(function)

    if find_index_function_arguments_count not in (1, 2, 3):
        raise ValueError("Invalid number of positional arguments in the 'find_index' function. The passed callback"
                         " function can have three positional arguments: the current element of the array, the index"
                         " of the current element, and the entire array.")

    if find_index_function_arguments_count == 1:
        for index, element in enumerate(self):
            if function(element):
                return index

    if find_index_function_arguments_count == 2:
        for index, element in enumerate(self):
            if function(element, index):
                return index

    elif find_index_function_arguments_count == 3:
        for index, element in enumerate(self):
            if function(element, index, self):
                return index

    return -1


def some_method(self: List, function: Callable) -> bool:
    some_method_function_arguments_count = get_function_positional_arguments_count(function)

    if some_method_function_arguments_count == 0 or some_method_function_arguments_count > 3:
        raise ValueError("Invalid number of positional arguments in the 'some' function. The passed callback function"
                         " can have three positional arguments: the current element of the array, the index of the"
                         " current element, and the entire array.")

    if some_method_function_arguments_count == 1:
        for element in self:
            if function(element):
                return True

    elif some_method_function_arguments_count == 2:
        for index, element in enumerate(self):
            if function(element, index):
                return True

    elif some_method_function_arguments_count == 3:
        for index, element in enumerate(self):
            if function(element, index, self):
                return True

    return False


def every_method(self: List, function: Callable) -> bool:
    every_method_function_arguments_count = get_function_positional_arguments_count(function)

    if every_method_function_arguments_count == 0 or every_method_function_arguments_count > 3:
        raise ValueError("Invalid number of positional arguments in the 'every' function. The passed callback function"
                         " can have three positional arguments: the current element of the array, the index of the"
                         " current element, and the entire array.")

    if every_method_function_arguments_count == 1:
        for element in self:
            if not function(element):
                return False

    elif every_method_function_arguments_count == 2:
        for index, element in enumerate(self):
            if not function(element, index):
                return False

    elif every_method_function_arguments_count == 3:
        for index, element in enumerate(self):
            if not function(element, index, self):
                return False

    return True


def flat_method(self: List, depth: Union[int, float] = 1) -> List:
    flatten = []

    def flat(arr, flat_depth):
        for element in arr:
            if type(element) is list and flat_depth >= 1:
                flat(element, flat_depth - 1)
            else:
                flatten.append(element)

    flat(self, depth)

    return flatten


def join_method(self: List, delimiter: str, cast_types: bool = False) -> str:
    """
    Since JavaScript has automatic typecasting to a string and it usually works correctly, but Python does not have such
    functionality, I decided to add an additional parameter that determines whether all array elements will be cast
    to a string type when concatenated.
    """

    if cast_types:
        stringified_array = list(map(lambda element: str(element), self))
        return delimiter.join(stringified_array)

    return delimiter.join(self)


def reversed_method(self: List) -> List:
    return self[::-1]


def reduce_method(self: List, function: Callable, initial_value: Any = None) -> Any:
    if not self and not initial_value:
        raise ValueError("Reduce of empty array with no initial value.")

    reduce_method_function_arguments_count = get_function_positional_arguments_count(function)

    if reduce_method_function_arguments_count not in (2, 3, 4):
        raise ValueError("Invalid number of positional arguments in 'reduce' function. The passed callback function"
                         " can have four positional arguments: accumulator, that accumulates the value returned by"
                         " callback function after visiting next element [required],"
                         " current element of the array [required],"
                         " index of the current element [optional],"
                         " and the entire array [optional].")

    it = iter(self)
    value = initial_value if initial_value is not None else next(it)
    start_index = 0 if initial_value is not None else 1

    if reduce_method_function_arguments_count == 2:
        return functools.reduce(function, it, value)

    elif reduce_method_function_arguments_count == 3:
        for element, index in zip(it, range(start_index, len(self))):
            value = function(value, element, index)

        return value

    elif reduce_method_function_arguments_count == 4:
        for element, index in zip(it, range(start_index, len(self))):
            value = function(value, element, index, self)

        return value


def reduce_right_method(self: List, function: Callable, initial_value: Any = None) -> Any:
    return reduce_method(reversed_method(self), function, initial_value=initial_value)


def concat_method(self: List, *args: Any, expand_strings: bool = False) -> List:
    concatenated = self[:]
    for arg in args:
        # Expand only iterables, but excluding strings, unless the corresponding flag is set
        if hasattr(arg,  '__iter__') and (not isinstance(arg, str) or expand_strings):
            concatenated += arg
        else:
            concatenated.append(arg)

    return concatenated


def slice_method(self: List, start: Optional[int] = None, end: Optional[int] = None) -> List:
    return self[start:end]


def includes_method(self: List, element: Any) -> bool:
    return element in self


def entries_method(self: List) -> List[Tuple[int, Any]]:
    return list(zip(range(len(self)), self))


def fill_method(self: List, value: Any, start: int = 0, end: Optional[int] = None) -> List:
    filled = self[:]

    if end is None or end > len(self):
        end = len(self)
    if start > end:
        return filled

    filled[start:end] = [value] * (end - start)
    return filled


def keys_method(self: List) -> List[int]:
    return [*range(len(self))]


def last_index_of_method(self: List, searched_element: Any, from_index: int = -1) -> int:
    array_len = len(self)

    '''
    Since it takes a long time to compare large iterable objects (strings, arrays, etc.), it makes sense to first
    reverse the main array and search in the built-in list.index method expanded from the end.
    '''
    if(type(searched_element) != 'type' or not hasattr(searched_element, '__len__') or len(searched_element) < 1000)\
            and from_index < 0:

        for index in range(array_len + from_index, -1, -1):
            if self[index] == searched_element:
                return index
        return -1

    try:
        if from_index >= 0:
            from_index = min(from_index, array_len - 1)
            return from_index - self[from_index::-1].index(searched_element)

        return array_len - self[from_index::-1].index(searched_element) + from_index

    except ValueError:
        return -1


def sorted_method(self: List, **kwargs) -> List:
    return sorted(self, **kwargs)


def to_string_method(self: List) -> str:
    return ','.join(map(lambda el: str(el), flat_method(self, float("Inf"))))


def copy_within_method(self: List, target: int, start: int = 0, end: Optional[int] = None) -> List:
    if end is None:
        end = len(self)

    copied_segment_length = end - start
    end_target = target + copied_segment_length
    if end_target > len(self):
        end_target = len(self)
        end = start + (end_target - target)

    copy = self.copy()
    copy[target:end_target] = self[start:end]

    return copy
