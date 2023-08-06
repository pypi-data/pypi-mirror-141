from abc import ABC
import abc
from typing import List, Optional, Union
from aiondao.libs.states import SimState
from aiondao.interfaces.simulate import ISimBlock, ISimTransform, IPipeline


class IPolicyBlock(ISimBlock):
    # Figure out if there's some policies
    def transform(self, state_space: SimState) -> SimState:

        return state_space


class IPolicyTransform(ISimTransform):

    # Figure out if there's some policies
    def transform(self, state_space: SimState) -> SimState:

        return super().transform(state_space)
