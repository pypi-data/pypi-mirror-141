from mesa.agent import Agent

# isort: off
from typing import cast

# isort: on


# from aiondao.agents.dummy import DummyAgent

from loguru import logger
from mesa import Agent
from aiondao.libs.states import SimState

from loguru import logger

ilog = logger.info


class DummyAgent(Agent):
    """An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

        logger.debug(f"Starting Dummy Model: {self.unique_id}")

    def step(self):
        self.model.commons = cast(SimState, self.model.commons)
        self.model.commons.unique_id += 1

        return super().step()
