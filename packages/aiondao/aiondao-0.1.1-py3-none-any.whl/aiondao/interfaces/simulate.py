"""Base blocks for simulation and changes the state of the model."""
import abc
from typing import List, Optional
from aiondao.libs.states import SimState


class ISimBlock(abc.ABC):
    """
    A simulation block is a part of the simulation that is executed in a single
    step. It recieves the state and returns the new state. It contains a single transformation that can get built upon over time.
    """

    @abc.abstractmethod
    def execute(self, state: SimState) -> Optional[SimState]:
        """
        The small units of work.
        """


class ISimTransform(ISimBlock, abc.ABC):
    def transform(self, state_space: SimState) -> SimState:
        updated: SimState = self.execute(state_space)
        assert (
            updated is not None
        ), "SimTransform must return a new state. None is not allowed"
        return updated


class IPipeline(ISimBlock, abc.ABC):
    def __init__(self, state_transforms: List[ISimTransform]) -> None:
        if not state_transforms:
            raise ValueError(
                "PolicySequential requires at least one state transform. Declaring it without using it is not allowed"
            )
        self.state_transforms: List[ISimTransform] = state_transforms

    def transform(self, state_space: SimState) -> SimState:
        for state_transformer in self.state_transforms:
            state_space = state_transformer.transform(state_space)
        return state_space
