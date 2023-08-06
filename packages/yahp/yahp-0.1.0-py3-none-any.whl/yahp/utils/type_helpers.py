# Copyright 2021 MosaicML. All Rights Reserved.

from __future__ import annotations

import json
from dataclasses import MISSING, Field
from enum import Enum
from typing import Any, Dict, Sequence, Tuple, Type, Union, cast

import yahp as hp
from yahp.utils.iter_helpers import ensure_tuple
from yahp.utils.typing_future import get_args, get_origin


class _JSONDict:  # sentential for representing JSON dictionary types
    pass


_PRIMITIVE_TYPES = (bool, int, float, str)


def safe_issubclass(item: Any, class_or_tuple: Union[Type[Any], Tuple[Type[Any], ...]]) -> bool:
    return isinstance(item, type) and issubclass(item, class_or_tuple)


def _is_valid_primitive(*types: Type[Any]) -> bool:
    # only one of (bool, int, float), and optionally string, is allowed
    if not all(x in _PRIMITIVE_TYPES for x in types):
        return False
    has_bool = bool in types
    has_int = int in types
    has_float = float in types
    if has_bool + has_int + has_float > 1:
        # Unions of bools, ints, and/or floats are not supported. Pick only one.
        return False
    return True


class HparamsType:
    """Wrapper to parse type annotations and determine type of field.

    HparamsType parses typing annotations and provides convenience methods
    to determine the field types.

    Args:
        item (type): Type annotation to parse.

    Attributes:
        types (List[Type]): The allowed types for this annotation, as a list.
            If the annotation is ``List[X]`` or ``Optional[X]``,
            then ``X`` is stored in this attributed.
            If the annotation is a ``Union[X, Y]``, then this attribute
            is ``[X, Y]``. None is never stored here;
            instead, see :attr:`is_optional`.
        is_optional (bool): Whether the annotation allows None.
        is_list (bool): Whether the annotation is a list.
    """

    def __init__(self, item: Type[Any]) -> None:
        self.types, self.is_optional, self.is_list = self._extract_type(item)
        if len(self.types) == 0:
            assert self.is_optional, 'invariant error'

    def _extract_type(self, item: Type[Any]) -> Tuple[Sequence[Type[Any]], bool, bool]:
        """Extracts the underlying types from a python typing object.

        Documentration is best given through examples:
        >>> _extract_type(bool) == ([bool], False, False)
        >>> _extract_type(Optional[bool])== ([bool], True, False)
        >>> _extract_type(List[bool])== ([bool], False, True)
        >>> _extract_type(List[Optional[bool]]) raises a TypeError, since Lists of optionals are not allowed by hparams
        >>> _extract_type(Optional[List[bool]]) == ([bool], True, True)
        >>> _extract_type(Optional[List[Union[str, int]]]) == ([str, int], True, True)
        >>> _extract_type(List[Union[str, int]]) == ([str, int], False, True)
        >>> _extract_type(Union[str, int]) == ([str, int], False, False)
        >>> _extract_type(Union[str, Enum]) raises a TypeError, since Enums cannot appear in non-optional Unions
        >>> _extract_type(Union[str, NoneType]) == ([str], True, False)
        >>> _extract_type(Union[str, Dataclass]) raises a TypeError, since Hparam dataclasses cannot appear in non-optional unions
        """
        origin = get_origin(item)
        if origin is None:
            # item must be simple, like None, int, float, str, Enum, or Hparams
            if item is None or item is type(None):
                return [], True, False
            if item not in _PRIMITIVE_TYPES and not safe_issubclass(item, (hp.Hparams, Enum)):
                raise TypeError(f'item of type ({item}) is not supported.')
            is_optional = False
            is_list = False
            return [item], is_optional, is_list
        if origin is Union:
            args = cast(Sequence[Any], get_args(item))
            is_optional = type(None) in args
            args_without_none = tuple(arg for arg in args if arg not in (None, type(None)))
            # all args in the union must be subclasses of one of the following subsets
            is_primitive = _is_valid_primitive(*args_without_none)
            is_enum = all(safe_issubclass(arg, Enum) for arg in args_without_none)
            is_hparams = all(safe_issubclass(arg, hp.Hparams) for arg in args_without_none)
            is_list = all(get_origin(arg) is list for arg in args_without_none)
            is_json_dict = all(get_origin(arg) is dict for arg in args_without_none)
            if is_primitive or is_hparams or is_enum:
                assert is_list is False
                return args_without_none, is_optional, is_list
            if is_list:
                # Need to validate that the underlying type of list is either 1) Primitive, 2) Union of primitives
                #                 assert len(args_without_none) == 1, "should only have one one"
                assert len(args_without_none) == 1, 'if here, should only have 1 non-none argument'
                list_arg = args_without_none[0]
                return self._get_list_type(list_arg), is_optional, is_list
            if is_json_dict:
                assert is_optional, 'if here, then must have been is_optional'
                assert not is_list, 'if here, then must not have been is_list'
                return [_JSONDict], is_optional, is_list
            raise TypeError(f'Invalid union type: {item}. Unions must be of primitive types')
        if origin is list:
            is_optional = False
            is_list = True
            return self._get_list_type(item), is_optional, is_list
        if origin is dict:
            is_optional = False
            is_list = False
            return [_JSONDict], is_optional, is_list
        raise TypeError(f'Unsupported type: {item}')

    def _get_list_type(self, list_arg: Type[Any]) -> Sequence[Type[Any]]:
        if get_origin(list_arg) is not list:
            raise TypeError('list_arg is not a List')
        list_args = get_args(list_arg)
        assert len(list_args) == 1, 'lists should have exactly one argument'
        list_item = list_args[0]
        error = TypeError(f'List of type {list_item} is unsupported. Lists must be of Hparams, Enum, or a valid union.')
        list_origin = get_origin(list_item)
        if list_origin is None:
            # Must be either primitive or hparams
            if list_item not in _PRIMITIVE_TYPES and not safe_issubclass(list_item, (hp.Hparams, Enum)):
                raise error
            return [list_item]
        if list_origin is Union:
            list_args = cast(Sequence[Any], get_args(list_item))
            is_primitive = _is_valid_primitive(*list_args)
            if not is_primitive:
                raise error
            return list_args
        raise error

    @property
    def is_hparams_dataclass(self) -> bool:
        """
        Whether it is a subclass of :class:`~yahp.hparams.Hparams`,
        or a list of :class:`~yahp.hparams.Hparams`.
        """
        return len(self.types) > 0 and all(safe_issubclass(t, hp.Hparams) for t in self.types)

    @property
    def is_json_dict(self) -> bool:
        """Whether it is a JSON Dictionary."""
        return len(self.types) > 0 and all(safe_issubclass(t, _JSONDict) for t in self.types)

    def convert(self, val: Any, field_name: str, *, wrap_singletons: bool = True) -> Any:
        """Attempt to convert an item into a type allowed by the annotation.

        Args:
            val (Any): Item to convert.
            field_name (str): Name for field being converted.
            wrap_singletons (bool, optional):
                If True (the default) and the field is a list, singletons will
                be wrapped into a list. Otherwise, raise a :class:`TypeError`.

        Raises:
            ValueError: Raised if :attr:`val` is None, but
                the annotation does not permit None.
            TypeError: Raised if :attr:`val` cannot be converted into a type
                specified by the annotation.

        Returns:
            The converted item.
        """
        # converts a value to the type specified by hparams
        # val can ether be a JSON or python representation for the value
        # If a singleton is given to a list, it will be converted to a list
        if self.is_optional:
            if is_none_like(val, allow_list=self.is_list):
                return None
        if not self.is_optional and val is None:
            raise ValueError(f'{field_name} is None, but a value is required.')
        if self.is_list:
            # If given a list, then return a list of converted values
            if wrap_singletons:
                return [
                    self.convert(x, f'{field_name}[{i}]', wrap_singletons=False)
                    for (i, x) in enumerate(ensure_tuple(val))
                ]
            elif isinstance(val, (tuple, list)):
                raise TypeError(f'{field_name} is a list, but wrap_singletons is false')
        if self.is_enum:
            # could be a list of enums too
            assert issubclass(self.type, Enum)
            enum_map: Dict[Union[str, Enum], Enum] = {k.name.lower(): k for k in self.type}
            enum_map.update({k.value: k for k in self.type})
            enum_map.update({k: k for k in self.type})
            if isinstance(val, str):  # if the val is a string, then check for a key match
                val = val.lower()
                if val not in enum_map:
                    possible_keys = [str(key) for key in enum_map.keys()]
                    raise ValueError(f"'{val}' is not a valid key. Choose on of {', '.join(possible_keys)}.")
            return enum_map[val]
        if self.is_hparams_dataclass:
            if isinstance(val, self.type):
                return val
            raise RuntimeError('convert() cannot be used with hparam dataclasses')
        if self.is_json_dict:
            if isinstance(val, str):
                val = json.loads(val)
            if not isinstance(val, dict):
                raise TypeError(f'{field_name} is not a dictionary')
            return val
        if self.is_primitive:
            # could be a list of primitives
            for t in (bool, float, int, str):
                # bool, float, and int are mutually exclusive
                if t in self.types:
                    try:
                        return to_bool(val) if t is bool else t(val)
                    except (TypeError, ValueError):
                        pass

            raise TypeError(f'Unable to convert value {val} for field {field_name} to type {self}')
        raise RuntimeError(f'Unknown type for field {field_name}')

    @property
    def is_enum(self) -> bool:
        """
        Whether the annotation allows for a subclass of :class:`Enum`,
        or a list of :class:`Enum`.
        """
        return len(self.types) > 0 and all(safe_issubclass(t, Enum) for t in self.types)

    @property
    def is_primitive(self) -> bool:
        """
        Whether the annotation allows for a
        :class:`bool`, :class:`int`, :class:`str`, or :class:`float`,
        or a list of such types.
        """
        return len(self.types) > 0 and all(safe_issubclass(t, _PRIMITIVE_TYPES) for t in self.types)

    @property
    def is_boolean(self) -> bool:
        """
        Whether the annotation allows for a :class:`bool`,
        or a list of :class:`bool`.
        """
        return len(self.types) > 0 and all(safe_issubclass(t, bool) for t in self.types)

    @property
    def type(self) -> Type[Any]:
        """
        The underlying type allowed by the annotation.
        If the annotation is a ``List[x]`` or ``Optional[X]``, then ``X`` is returned.

        This property is only available if the annotation is not a union
        of multiple types. For these cases, see :attr:`types`.
        """
        if len(self.types) != 1:
            # self.types it not 1 in the case of unions
            raise RuntimeError('.type is not defined for unions')
        return self.types[0]

    def __str__(self) -> str:
        ans = None
        if self.is_primitive:  # str, float, int, bool
            if len(self.types) > 1:
                ans = f"{' | '.join(t.__name__ for t in self.types)}"
            else:
                ans = self.type.__name__

        if self.is_enum:
            assert issubclass(self.type, Enum)
            enum_values_string = ', '.join([x.name for x in self.type])
            ans = f'{self.type.__name__}{{{enum_values_string}}}'

        if self.is_hparams_dataclass:
            ans = self.type.__name__

        if self.is_json_dict:
            ans = 'JSON'

        if ans is None:
            # always None
            return 'None'

        if self.is_list:
            ans = f'List[{ans}]'

        if self.is_optional:
            ans = f'Optional[{ans}]'
        return ans


def is_field_required(f: Field[Any]) -> bool:
    """
    Returns whether a field is required
    (i.e. does not have a default value).

    Args:
        f (Field): The field.
    """
    return get_default_value(f) == MISSING


def get_default_value(f: Field[Any]) -> Any:
    """Returns an instance of a default value for a field.

    Args:
        f (Field): The field.
    """
    if f.default != MISSING:
        return f.default
    if f.default_factory != MISSING:
        return f.default_factory()
    return MISSING


def to_bool(x: Any):
    """Converts a value to a boolean

    Args:
        x (object): Value to attempt to convert to a bool.
    """
    if isinstance(x, str):
        x = x.lower()
    if x in ('t', 'true', 'y', 'yes', 1, True):
        return True
    if x in ('f', 'false', 'n', 'no', 0, False):
        return False
    raise TypeError(f'Could not parse {x} as bool')


def is_none_like(x: Any, *, allow_list: bool) -> bool:
    """Returns whether a value is ``None``, ``"none"``, ``[""]``, ``["none"]``, or has been marked as a missing field.

    Args:
        x (object): Value to examine.
        allow_list (bool): Whether to treat ``[""]``, or ``["none"]`` as ``None``.
    """
    if x is None or x is MISSING:
        return True
    if isinstance(x, str) and x.lower() in ['', 'none']:
        return True
    if x == MISSING:
        return True
    if allow_list and isinstance(x, (tuple, list)) and len(x) == 1:
        return is_none_like(x[0], allow_list=allow_list)
    return False
