from typing import List, Optional
from aiondao.libs.states import SimState
from aiondao.interfaces.policy import IPipeline
from aiondao.interfaces.simulate import ISimTransform


class Sequential(IPipeline):
    """Gets the current state anc makes updates to it. Not changing system much compared to the original code so it will happen in batch."""

    def __init__(self, state_transforms: List[ISimTransform]) -> None:
        super().__init__(state_transforms)

    def execute(self, state: SimState) -> Optional[SimState]:
        return super().execute(state)

    def transform(self, state_space: SimState) -> SimState:
        for state_transformer in self.state_transforms:
            state_space = state_transformer.transform(state_space)
        return state_space
