"""Global imports to reduce typing."""
# A tacky tactic I picked up to reduce the number of imports to manually do.
# Can use autoflake expand_star_imports to get the specific imports.
__version__ = "0.1.0"

# isort: off
from auto_all import end_all, start_all
from pydantic.main import ModelMetaclass
from pydantic.fields import FieldInfo, ModelField
from pydantic.typing import AnyCallable

start_all(globals())

# isort: on
import abc
import math
from datetime import timedelta
from enum import Enum
from functools import partial
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    List,
    Mapping,
    NamedTuple,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
)

import pandas as pd
from cytoolz.dicttoolz import itemfilter, valfilter, keyfilter
from decorator import decorator
from loguru import logger
from pydantic import (
    BaseConfig,
    BaseModel,
    Extra,
    Field,
    parse_obj_as,
    root_validator,
    PrivateAttr,
    validator,
)
from pydantic.dataclasses import dataclass
from pydantic.generics import GenericModel
from toolz import keyfilter
from pydantic import BaseModel
import networkx as nx

# from toolz import valfilter

ROOT = Path(__file__).parent


CallableAny = Callable[..., Any]
OptCallAny = Optional[CallableAny]
TupleAny = Tuple[str, Any]
StateSP = TypeVar("StateSP")
SysParams = TypeVar("SysParams")
PolicySP = TypeVar("PolicySP")
DictAny = Dict[str, Any]
RandomNumCallable = Callable[..., float]


iprint = logger.info
ilog = logger.info


class StrEnum(str, Enum):
    """Enum with string values."""


class BroadConfig(BaseConfig):
    arbitrary_types_allowed = True
    underscore_attrs_are_private = True


class cfgall(BroadConfig):

    extra = Extra.allow


class cfgign(BroadConfig):
    extra = Extra.ignore


class autovalid(BroadConfig):
    """Automatically validate assigned values."""

    arbitrary_types_allowed = True
    extra = Extra.allow
    validate_assignment = True


class iautovalid(BaseConfig):
    """Automatically validate assigned values. with ignore extra."""

    extra = Extra.ignore
    validate_assignment = True


# import cytoolz
from devtools import debug


class RelaxedModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow
        # validate_assignment = True


_T = TypeVar("_T")


def __dataclass_transform__(
    *,
    eq_default: bool = True,
    order_default: bool = False,
    kw_only_default: bool = False,
    field_descriptors: Tuple[Union[type, Callable[..., Any]], ...] = (()),
) -> Callable[[_T], _T]:
    return lambda a: a


@__dataclass_transform__(field_descriptors=(Field, FieldInfo))
class SyncMetadata(ModelMetaclass):
    def __new__(cls, name, bases, namespace, **kwargs):
        """Completely ignore the metadata."""
        return super().__new__(cls, name, bases, namespace, **kwargs)


class SyncModel(BaseModel, metaclass=SyncMetadata):
    __model_maps__: ClassVar[Dict[Union[str, int], Any]] = {}

    if TYPE_CHECKING:
        # populated by the metaclass, defined here to help IDEs only
        __fields__: ClassVar[Dict[str, ModelField]] = {}
        __include_fields__: ClassVar[Optional[Mapping[str, Any]]] = None
        __exclude_fields__: ClassVar[Optional[Mapping[str, Any]]] = None
        __validators__: ClassVar[Dict[str, AnyCallable]] = {}
        __pre_root_validators__: ClassVar[List[AnyCallable]]
        __post_root_validators__: ClassVar[List[Tuple[bool, AnyCallable]]]
        __config__: ClassVar[Type[BaseConfig]] = BaseConfig
        __json_encoder__: ClassVar[Callable[[Any], Any]] = lambda x: x
        __schema_cache__: ClassVar["DictAny"] = {}
        __custom_root_type__: ClassVar[bool] = False

    class Config:
        extra = Extra.allow
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True


@__dataclass_transform__(field_descriptors=(Field, FieldInfo))
class BorgModel(SyncModel, metaclass=SyncMetadata):
    __shared_state__: ClassVar[Dict[str, Any]] = {}

    # New class __new__  that inherits the shares state
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__sync_shared()

    def __setattr__(self, name, value):
        resp = super().__setattr__(name, value)
        self.__sync_shared()
        return resp

    def __getattr__(self, name):
        if name in self.__shared_state__:
            return self.__shared_state__[name]
        try:
            return self.__dict__[name]

        except KeyError as ae:
            raise AttributeError(f"The attribute '{name}' is not defined")

    def __sync_shared(self):
        self.__shared_state__.update(valfilter(lambda x: x is not None, self.__dict__))


@__dataclass_transform__(field_descriptors=(Field, FieldInfo))
class BorgIdModel(SyncModel, metaclass=SyncMetadata):
    # If there's a crazy ID I will
    __shared_state__: ClassVar[Dict[str, Any]] = {}
    crazy_id: Optional[int] = None
    # New class __new__  that inherits the shares state
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        # __pydantic_self__.crazy_id: Optional[int] = None
        if __pydantic_self__.is_crazy():
            __pydantic_self__.__sync_shared()

        # __pydantic_self__.__crazy_id = self.__id
        # debug(__pydantic_self__.__shared_state__)

    def is_crazy(self) -> bool:
        """Detects if there's an id set.

        Returns:
            bool: _description_
        """
        return bool(self.crazy_id)

    # @property
    # def crazy_id(self):
    #     """The crazy_id property."""
    #     return self._crazy_id

    # @crazy_id.setter
    # def crazy_id(self, value: int):
    #     self._crazy_id = value
    #     self.__sync_shared()
    #     debug(self.__shared_state__)

    def is_within(self) -> bool:
        if self.is_crazy() and self.crazy_id in self.__shared_state__:
            return True
        return False

    def __setattr__(self, name, value):
        resp = super().__setattr__(name, value)
        if self.is_crazy():
            self.__sync_shared()

        return resp

    def __getattr__(self, name):
        if (
            self.is_crazy()
            and self.is_within()
            and name in self.__shared_state__[self.crazy_id]
        ):
            return self.__shared_state__.get(self.crazy_id, {}).get(name, None)

        try:
            return self.__dict__[name]

        except KeyError as ae:
            raise AttributeError(f"The attribute '{name}' is not defined")

    def __sync_shared(self):
        idx = self.crazy_id
        # logger.warning(idx)
        removed_none = valfilter(lambda x: (x is not None), self.__dict__)
        removed_id = keyfilter(lambda x: x != "_crazy_id", removed_none)
        curr = self.__shared_state__.get(idx, {})
        curr.update(removed_none)
        # updated_dict_state = self.__shared_state__.get(idx, {}).update(removed_id)
        # debug(curr)
        self.__shared_state__[self.crazy_id] = curr
        # updated_dict_state


# isort: off
end_all(globals())
# isort: on
