__version__ = "0.1.0"

# from typing import Any, Callable, Type, Union, TYPE_CHECKING, TypeVar, cast
# from pydantic import BaseConfig, Extra
# from pydantic.dataclasses import dataclass as _dataclass

# if TYPE_CHECKING:
#     from typing import Dataclass


# from functools import partial


# class BroadConfig(BaseConfig):
#     arbitrary_types_allowed = True
#     underscore_attrs_are_private = True


# class cfgall(BroadConfig):

#     extra = Extra.allow


# class cfgign(BroadConfig):
#     extra = Extra.ignore


# class autovalid(BaseConfig):
#     """Automatically validate assigned values."""

#     extra = Extra.allow
#     validate_assignment = True


# class iautovalid(BaseConfig):
#     """Automatically validate assigned values. with ignore extra."""

#     extra = Extra.ignore
#     validate_assignment = True


# dataclass = partial(_dataclass, config=autovalid)


# dataclass = cast(_dataclass, dataclass)
# # dataclass = dataclass(config=autovalid)
# # idataclass = dataclass(config=autovalid)
