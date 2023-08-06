# Copyright 2021 MosaicML. All Rights Reserved.

from __future__ import annotations

import argparse
import logging
import os
import pathlib
import sys
import textwrap
import warnings
from dataclasses import MISSING, dataclass, fields
from typing import (TYPE_CHECKING, Any, Dict, List, Optional, Sequence, TextIO, Tuple, Type, TypeVar, Union,
                    get_type_hints)

import yaml

import yahp as hp
from yahp.create.argparse import (ArgparseNameRegistry, ParserArgument, get_commented_map_options_from_cli,
                                  get_hparams_file_from_cli, retrieve_args)
from yahp.inheritance import load_yaml_with_inheritance
from yahp.utils.iter_helpers import ensure_tuple, extract_only_item_from_dict, list_to_deduplicated_dict
from yahp.utils.type_helpers import HparamsType, get_default_value, is_field_required, is_none_like

if TYPE_CHECKING:
    from yahp.types import JSON, HparamsField

THparams = TypeVar('THparams', bound='hp.Hparams')


class _MissingRequiredFieldException(ValueError):
    pass


@dataclass
class _DeferredCreateCall:
    hparams_cls: Type[hp.Hparams]
    data: Dict[str, JSON]
    prefix: List[str]
    parser_args: Optional[Sequence[ParserArgument]]


def _emit_should_be_dict_warning(arg_name: str):
    warnings.warn(f'MalformedYAMLWarning: {arg_name} should be a dict.')


def _get_split_key(key: str, splitter: str = '+') -> Tuple[str, Any]:
    """ Gets the prefix key and any label after the splitter """

    splits = key.split(splitter, 1)
    if len(splits) > 1:
        return (splits[0], splits[1])
    else:
        return (splits[0], None)


logger = logging.getLogger(__name__)


def _create(
    *,
    cls: Type[THparams],
    data: Dict[str, JSON],
    parsed_args: Dict[str, str],
    cli_args: Optional[List[str]],
    prefix: List[str],
    argparse_name_registry: ArgparseNameRegistry,
    argparsers: List[argparse.ArgumentParser],
) -> THparams:
    """Helper method to recursively create an instance of the :class:`~yahp.hparams.Hparams`.

    Args:
        data (Dict[str, JSON]):
            A JSON dictionary of values to use to initialize the class.
        parsed_args (Dict[str, str]):
            Parsed args for this class.
        cli_args (Optional[List[str]]):
            A list of cli args. This list is modified in-place,
            and all used arguments are removed from the list.
            Should be None if no cli args are to be used.
        prefix (List[str]):
            The prefix corresponding to the subset of ``cli_args``
            that should be used to instantiate this class.
        argparse_name_registry (_ArgparseNameRegistry):
            A registry to track CLI argument names.
        argparsers (List[argparse.ArgumentParser]):
            A list of :class:`~argparse.ArgumentParser` instances,
            which is extended in-place.

    Returns:
        An instance of the class.
    """
    kwargs: Dict[str, HparamsField] = {}
    deferred_create_calls: Dict[str, Union[_DeferredCreateCall,  # singleton field
                                           List[_DeferredCreateCall],  # list field
                                          ]] = {}

    # keep track of missing required fields so we can build a nice error message
    missing_required_fields: List[str] = []

    cls.validate_keys(list(data.keys()), allow_missing_keys=True)
    field_types = get_type_hints(cls)
    for f in fields(cls):
        if not f.init:
            continue
        prefix_with_fname = list(prefix) + [f.name]
        try:
            ftype = HparamsType(field_types[f.name])
            full_name = '.'.join(prefix_with_fname)
            env_name = full_name.upper().replace('.', '_')  # dots are not (easily) allowed in env variables
            if full_name in parsed_args and parsed_args[full_name] != MISSING:
                # use CLI args first
                argparse_or_yaml_value = parsed_args[full_name]
            elif f.name in data:
                # then use YAML
                argparse_or_yaml_value = data[f.name]
            elif env_name in os.environ:
                # then use environment variables
                argparse_or_yaml_value = os.environ[env_name]
            else:
                # otherwise, set it as MISSING so the default will be used
                argparse_or_yaml_value = MISSING

            if not ftype.is_hparams_dataclass:
                if argparse_or_yaml_value == MISSING:
                    if not is_field_required(f):
                        # if it's a primitive and there's a default value,
                        # then convert and use it.
                        # Sometimes primitives will not have correct default values
                        # (e.g. type is float, but the default is an int)
                        kwargs[f.name] = ftype.convert(get_default_value(f), full_name)
                else:
                    kwargs[f.name] = ftype.convert(argparse_or_yaml_value, full_name)
            else:
                if f.name not in cls.hparams_registry:
                    # concrete, singleton hparams
                    # list of concrete hparams
                    # potentially none
                    if not ftype.is_list:
                        # concrete, singleton hparams
                        # potentially none. If cli args specify a child field, implicitly enable optional parent class
                        is_none = ftype.is_optional and is_none_like(argparse_or_yaml_value, allow_list=ftype.is_list)
                        if is_none and cli_args is not None:
                            for cli_arg in cli_args:
                                if cli_arg.lstrip('-').startswith(f.name):
                                    is_none = False
                                    break
                        if is_none:
                            # none
                            kwargs[f.name] = None
                        else:
                            # concrete, singleton hparams
                            sub_yaml = data.get(f.name)
                            if sub_yaml is None:
                                sub_yaml = {}
                            if not isinstance(sub_yaml, dict):
                                raise ValueError(f'{full_name} must be a dict in the yaml')
                            assert issubclass(ftype.type, hp.Hparams)
                            deferred_create_calls[f.name] = _DeferredCreateCall(
                                hparams_cls=ftype.type,
                                data=sub_yaml,
                                prefix=prefix_with_fname,
                                parser_args=retrieve_args(cls=ftype.type,
                                                          prefix=prefix_with_fname,
                                                          argparse_name_registry=argparse_name_registry),
                            )
                    else:
                        # list of concrete hparams
                        # potentially none
                        # concrete lists not added to argparse, so just load the yaml
                        if ftype.is_optional and is_none_like(argparse_or_yaml_value, allow_list=ftype.is_list):
                            # none
                            kwargs[f.name] = None
                        else:
                            # list of concrete hparams
                            # concrete lists not added to argparse, so just load the yaml
                            sub_yaml = data.get(f.name)
                            # yaml should be a dictionary. We'll discard the keys
                            if sub_yaml is None:
                                sub_yaml = {}

                            if isinstance(sub_yaml, list):
                                _emit_should_be_dict_warning(full_name)
                                sub_yaml = list_to_deduplicated_dict(sub_yaml)

                            if not isinstance(sub_yaml, dict):
                                raise TypeError(f'{full_name} must be a dict in the yaml')

                            deferred_calls: List[_DeferredCreateCall] = []
                            for (key, sub_yaml_item) in sub_yaml.items():
                                if sub_yaml_item is None:
                                    sub_yaml_item = {}
                                if not isinstance(sub_yaml_item, dict):
                                    raise TypeError(f'{full_name} must be a dict in the yaml')
                                assert issubclass(ftype.type, hp.Hparams)
                                deferred_calls.append(
                                    _DeferredCreateCall(
                                        hparams_cls=ftype.type,
                                        data=sub_yaml_item,
                                        prefix=prefix_with_fname + [key],
                                        parser_args=None,
                                    ))
                            deferred_create_calls[f.name] = deferred_calls
                else:
                    # abstract, singleton hparams
                    # list of abstract hparams
                    # potentially none
                    if not ftype.is_list:
                        # abstract, singleton hparams
                        # potentially none
                        if ftype.is_optional and is_none_like(argparse_or_yaml_value, allow_list=ftype.is_list):
                            # none
                            kwargs[f.name] = None
                        else:
                            # abstract, singleton hparams
                            # look up type in the registry
                            # should only have one key in the dict
                            # argparse_or_yaml_value is a str if argparse, or a dict if yaml
                            if argparse_or_yaml_value == MISSING:
                                # use the hparams default
                                continue
                            if argparse_or_yaml_value is None:
                                raise ValueError(f'Field {full_name} is required and cannot be None.')
                            if isinstance(argparse_or_yaml_value, str):
                                key = argparse_or_yaml_value
                            else:
                                if not isinstance(argparse_or_yaml_value, dict):
                                    raise ValueError(
                                        f'Field {full_name} must be a dict with just one key if specified in the yaml')
                                try:
                                    key, _ = extract_only_item_from_dict(argparse_or_yaml_value)
                                except ValueError as e:
                                    raise ValueError(f'Field {full_name} ' + e.args[0])
                            yaml_val = data.get(f.name)
                            if yaml_val is None:
                                yaml_val = {}
                            if not isinstance(yaml_val, dict):
                                raise ValueError(
                                    f"Field {'.'.join(prefix_with_fname)} must be a dict if specified in the yaml")
                            yaml_val = yaml_val.get(key)
                            if yaml_val is None:
                                yaml_val = {}
                            if not isinstance(yaml_val, dict):
                                raise ValueError(
                                    f"Field {'.'.join(prefix_with_fname + [key])} must be a dict if specified in the yaml"
                                )
                            deferred_create_calls[f.name] = _DeferredCreateCall(
                                hparams_cls=cls.hparams_registry[f.name][key],
                                prefix=prefix_with_fname + [key],
                                data=yaml_val,
                                parser_args=retrieve_args(cls=cls.hparams_registry[f.name][key],
                                                          prefix=prefix_with_fname + [key],
                                                          argparse_name_registry=argparse_name_registry),
                            )
                    else:
                        # list of abstract hparams
                        # potentially none
                        if ftype.is_optional and is_none_like(argparse_or_yaml_value, allow_list=ftype.is_list):
                            # none
                            kwargs[f.name] = None
                        else:
                            # list of abstract hparams
                            # argparse_or_yaml_value is a List[str] if argparse, or a List[Dict[str, Hparams]] if yaml
                            if argparse_or_yaml_value == MISSING:
                                # use the hparams default
                                continue

                            # First get the keys
                            # Argparse has precedence. If there are keys defined in argparse, use only those
                            # These keys will determine what is loaded
                            if argparse_or_yaml_value is None:
                                raise ValueError(f'Field {full_name} is required and cannot be None.')
                            if isinstance(argparse_or_yaml_value, list):
                                # Convert from list of single element dictionaries to dict, preserving duplicates
                                argparse_or_yaml_value = list_to_deduplicated_dict(argparse_or_yaml_value,
                                                                                   allow_str=True)

                            if not isinstance(argparse_or_yaml_value, dict):
                                raise ValueError(f'Field {full_name} should be a dict')

                            keys = list(argparse_or_yaml_value.keys())

                            # Now, load the values for these keys
                            yaml_val = data.get(f.name)
                            if yaml_val is None:
                                yaml_val = {}
                            if isinstance(yaml_val, list):
                                _emit_should_be_dict_warning(full_name)
                                yaml_val = list_to_deduplicated_dict(yaml_val)
                            if not isinstance(yaml_val, dict):
                                raise ValueError(
                                    f"Field {'.'.join(prefix_with_fname)} must be a dict if specified in the yaml")

                            deferred_calls: List[_DeferredCreateCall] = []

                            for key in keys:
                                # Use the order of keys
                                key_yaml = yaml_val.get(key)
                                if key_yaml is None:
                                    key_yaml = {}
                                if not isinstance(key_yaml, dict):
                                    raise ValueError(
                                        textwrap.dedent(f"""Field {'.'.join(prefix_with_fname + [key])}
                                        must be a dict if specified in the yaml"""))
                                split_key, _ = _get_split_key(key)
                                deferred_calls.append(
                                    _DeferredCreateCall(
                                        hparams_cls=cls.hparams_registry[f.name][split_key],
                                        prefix=prefix_with_fname + [key],
                                        data=key_yaml,
                                        parser_args=retrieve_args(
                                            cls=cls.hparams_registry[f.name][split_key],
                                            prefix=prefix_with_fname + [key],
                                            argparse_name_registry=argparse_name_registry,
                                        ),
                                    ))
                            deferred_create_calls[f.name] = deferred_calls
        except _MissingRequiredFieldException as e:
            missing_required_fields.extend(e.args)
            # continue processing the other fields and gather everything together

    if cli_args is None:
        for fname, create_calls in deferred_create_calls.items():
            sub_hparams = [
                _create(
                    cls=deferred_call.hparams_cls,
                    data=deferred_call.data,
                    parsed_args={},
                    cli_args=None,
                    prefix=deferred_call.prefix,
                    argparse_name_registry=argparse_name_registry,
                    argparsers=argparsers,
                ) for deferred_call in ensure_tuple(create_calls)
            ]
            if isinstance(create_calls, list):
                kwargs[fname] = sub_hparams
            else:
                kwargs[fname] = sub_hparams[0]
    else:
        all_args: List[ParserArgument] = []
        for fname, create_calls in deferred_create_calls.items():
            for create_call in ensure_tuple(create_calls):
                if create_call.parser_args is not None:
                    all_args.extend(create_call.parser_args)
        argparse_name_registry.assign_shortnames()
        for fname, create_calls in deferred_create_calls.items():
            # TODO parse args from
            sub_hparams: List[hp.Hparams] = []
            for create_call in ensure_tuple(create_calls):
                if create_call.parser_args is None:
                    parsed_arg_dict = {}
                else:
                    parser = argparse.ArgumentParser(add_help=False)
                    argparsers.append(parser)
                    group = parser.add_argument_group(title='.'.join(create_call.prefix),
                                                      description=create_call.hparams_cls.__name__)
                    for args in create_call.parser_args:
                        for arg in ensure_tuple(args):
                            arg.add_to_argparse(group)
                    parsed_arg_namespace, cli_args[:] = parser.parse_known_args(cli_args)
                    parsed_arg_dict = vars(parsed_arg_namespace)
                sub_hparams.append(
                    _create(
                        cls=create_call.hparams_cls,
                        data=create_call.data,
                        parsed_args=parsed_arg_dict,
                        cli_args=cli_args,
                        prefix=create_call.prefix,
                        argparse_name_registry=argparse_name_registry,
                        argparsers=argparsers,
                    ))
            if isinstance(create_calls, list):
                kwargs[fname] = sub_hparams
            else:
                kwargs[fname] = sub_hparams[0]

    for f in fields(cls):
        if not f.init:
            continue
        prefix_with_fname = '.'.join(list(prefix) + [f.name])
        if f.name not in kwargs:
            if f.default == MISSING and f.default_factory == MISSING:
                missing_required_fields.append(prefix_with_fname)
            # else:
            #     warnings.warn(f"DefaultValueWarning: Using default value for {prefix_with_fname}. "
            #                   "Using default values is not recommended as they may change between versions.")
    if len(missing_required_fields) > 0:
        # if there are any missing fields from this class, or optional but partially-filled-in subclasses,
        # then propegate back the missing fields
        raise _MissingRequiredFieldException(*missing_required_fields)
    return cls(**kwargs)


def _add_help(argparsers: Sequence[argparse.ArgumentParser], cli_args: Sequence[str]) -> None:
    """Add an :class:`~argparse.ArgumentParser` that adds help.

    Args:
        argparsers (Sequence[argparse.ArgumentParser]): List of :class:`~argparse.ArgumentParser`s
            to extend.
    """
    help_argparser = argparse.ArgumentParser(parents=argparsers)
    help_argparser.parse_known_args(args=cli_args)  # Will print help and exit if the "--help" flag is present


def _get_remaining_cli_args(cli_args: Union[List[str], bool]) -> List[str]:
    if cli_args is True:
        return sys.argv[1:]  # remove the program name
    if cli_args is False:
        return []
    return list(cli_args)


def create(
    cls: Type[THparams],
    data: Optional[Dict[str, JSON]] = None,
    f: Union[str, TextIO, pathlib.PurePath, None] = None,
    cli_args: Union[List[str], bool] = True,
) -> THparams:
    """Create a instance of :class:`~yahp.hparams.Hparams`.

    Args:
        f (Union[str, None, TextIO, pathlib.PurePath], optional):
            If specified, load values from a YAML file.
            Can be either a filepath or file-like object.
            Cannot be specified with ``data``.
        data (Optional[Dict[str, JSON]], optional):
            f specified, uses this dictionary for instantiating
            the :class:`~yahp.hparams.Hparams`. Cannot be specified with ``f``.
        cli_args (Union[List[str], bool], optional): CLI argument overrides.
            Can either be a list of CLI argument,
            True (the default) to load CLI arguments from ``sys.argv``,
            or False to not use any CLI arguments.

    Returns:
        THparams: An instance of :class:`~yahp.hparams.Hparams`.
    """
    argparsers: List[argparse.ArgumentParser] = []
    remaining_cli_args = _get_remaining_cli_args(cli_args)
    try:
        hparams, output_f = _get_hparams(cls=cls,
                                         data=data,
                                         f=f,
                                         remaining_cli_args=remaining_cli_args,
                                         argparsers=argparsers)
    except _MissingRequiredFieldException as e:
        _add_help(argparsers, remaining_cli_args)
        missing_fields = f"{', '.join(e.args)}"
        raise ValueError(
            textwrap.dedent(f"""The following required fields were not included in the yaml nor the CLI arguments:
            {missing_fields}""")) from e
    _add_help(argparsers, remaining_cli_args)

    # Only if successful, warn for extra cli arguments
    # If there is an error, then valid cli args may not have been discovered
    for arg in remaining_cli_args:
        warnings.warn(f'ExtraArgumentWarning: {arg} was not used')

    if output_f is not None:
        if output_f == 'stdout':
            print(hparams.to_yaml(), file=sys.stdout)
        elif output_f == 'stderr':
            print(hparams.to_yaml(), file=sys.stderr)
        else:
            with open(output_f, 'x') as f:
                f.write(hparams.to_yaml())
        sys.exit(0)

    return hparams


def _get_hparams(
    cls: Type[THparams],
    data: Optional[Dict[str, JSON]],
    f: Union[str, TextIO, pathlib.PurePath, None],
    remaining_cli_args: List[str],
    argparsers: List[argparse.ArgumentParser],
) -> Tuple[THparams, Optional[str]]:
    argparse_name_registry = ArgparseNameRegistry()

    cm_options = get_commented_map_options_from_cli(
        cli_args=remaining_cli_args,
        argparse_name_registry=argparse_name_registry,
        argument_parsers=argparsers,
    )
    if cm_options is not None:
        output_file, interactive, add_docs = cm_options
        print(f'Generating a template for {cls.__name__}')
        if output_file == 'stdout':
            cls.dump(add_docs=add_docs, interactive=interactive, output=sys.stdout)
        elif output_file == 'stderr':
            cls.dump(add_docs=add_docs, interactive=interactive, output=sys.stderr)
        else:
            with open(output_file, 'x') as f:
                cls.dump(add_docs=add_docs, interactive=interactive, output=f)
        # exit so we don't attempt to parse and instantiate if generate template is passed
        print()
        print('Finished')
        sys.exit(0)

    cli_f, output_f = get_hparams_file_from_cli(cli_args=remaining_cli_args,
                                                argparse_name_registry=argparse_name_registry,
                                                argument_parsers=argparsers)
    if cli_f is not None:
        if f is not None:
            raise ValueError('File cannot be specified via both function arguments and the CLI')
        f = cli_f

    if f is not None:
        if data is not None:
            raise ValueError(
                textwrap.dedent(f"""Since a hparams file was specified via
                {'function arguments' if cli_f is None else 'the CLI'}, `data` must be None."""))
        if isinstance(f, pathlib.PurePath):
            f = str(f)
        if isinstance(f, str):
            data = load_yaml_with_inheritance(f)
        else:
            data = yaml.full_load(f)
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise TypeError('`data` must be a dict or None')

    # Parse args based on class cdefinition
    main_args = retrieve_args(cls=cls, prefix=[], argparse_name_registry=argparse_name_registry)
    parser = argparse.ArgumentParser(add_help=False)
    argparsers.append(parser)
    group = parser.add_argument_group(title=cls.__name__)
    for arg in main_args:
        arg.add_to_argparse(group)
    parsed_arg_namespace, remaining_cli_args[:] = parser.parse_known_args(remaining_cli_args)
    parsed_arg_dict = vars(parsed_arg_namespace)

    return _create(cls=cls,
                   data=data,
                   cli_args=remaining_cli_args,
                   prefix=[],
                   parsed_args=parsed_arg_dict,
                   argparse_name_registry=argparse_name_registry,
                   argparsers=argparsers), output_f


def get_argparse(
    cls: Type[THparams],
    data: Optional[Dict[str, JSON]] = None,
    f: Union[str, TextIO, pathlib.PurePath, None] = None,
    cli_args: Union[List[str], bool] = True,
) -> argparse.ArgumentParser:
    """Get an :class:`~argparse.ArgumentParser` containing all CLI arguments.

    Args:
        f (Union[str, None, TextIO, pathlib.PurePath], optional):
            If specified, load values from a YAML file.
            Can be either a filepath or file-like object.
            Cannot be specified with ``data``.
        data (Optional[Dict[str, JSON]], optional):
            f specified, uses this dictionary for instantiating
            the :class:`~yahp.hparams.Hparams`. Cannot be specified with ``f``.
        cli_args (Union[List[str], bool], optional): CLI argument overrides.
            Can either be a list of CLI argument,
            `true` (the default) to load CLI arguments from `sys.argv`,
            or `false` to not use any CLI arguments.

    Returns:
        argparse.ArgumentParser: An argparser with all CLI arguments, but without any help.
    """
    argparsers: List[argparse.ArgumentParser] = []

    remaining_cli_args = _get_remaining_cli_args(cli_args)

    try:
        _get_hparams(cls=cls, data=data, f=f, remaining_cli_args=remaining_cli_args, argparsers=argparsers)
    except _MissingRequiredFieldException:
        pass
    helpless_parent_argparse = argparse.ArgumentParser(add_help=False, parents=argparsers)
    return helpless_parent_argparse
