"""
The following code was adapted from the Bank Reserves model included in Netlogo
Model information can be found at: http://ccl.northwestern.edu/netlogo/models/BankReserves
Accessed on: November 2, 2017
Author of NetLogo code:
    Wilensky, U. (1998). NetLogo Bank Reserves model.
    http://ccl.northwestern.edu/netlogo/models/BankReserves.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

# isort: off
from typing import Iterable, cast
from aiondao._imports import *

# isort: on
import random

import numpy as np
from devtools import debug

from aiondao.agents.members import Participant

from aiondao.agents.commons import (
    CommonAgent,
    create_token_batches,
)

from loguru import logger
from mesa import Agent, Model
from mesa.time import RandomActivation, BaseScheduler
from aiondao.utils.networking import bootstrap_network, get_participants
from aiondao.libs.states import CommonsConfig, SimState
from aiondao.interfaces.models import IEconomy
from aiondao.libs.monitors import (
    get_num_rich_agents,
    get_num_poor_agents,
    get_num_mid_agents,
    get_total_savings,
    get_total_wallets,
    get_total_money,
    get_total_loans,
)
from aiondao.libs.bootloader import BootstrapSimulation
from aiondao.policies.transformer import (
    SyncState,
    CreateParticipant,
    CreateProposal,
    CreateFunding,
    ProcessActiveProposals,
    ParticipantVoting,
    ProposalFunding,
    ParticipantSentiment,
)
from aiondao.libs.pipes import Sequential
from aiondao.libs.graph import GraphORM

from aiondao.libs.states import SimState, StepSpace


class _AionEconomy(IEconomy, Model):

    schedule: "BaseScheduler"
    state: "SimState"

    @property
    def gfx(self) -> GraphORM:
        return GraphORM(net=self.state.network)

    @property
    def booter(self) -> BootstrapSimulation:
        if not hasattr(self, "_bootstrapper"):
            self._bootstrapper = BootstrapSimulation()
        return self._bootstrapper

    def start_step(self):
        pass
        # return super().start_step()

    def end_step(self):
        pass


class AionEconomy(_AionEconomy):
    """Transferred DAO"""

    """init parameters "init_people", "rich_threshold", and "reserve_percent"
       are all UserSettableParameters"""
    __slots__ = ["state", "params", "schedule", "policies", "count"]

    def __init__(self, params: CommonsConfig):
        super(AionEconomy, self).__init__()
        self.required()
        self.state: SimState = self.bootstrap(params)

        self.commons: CommonAgent = self.state.commons
        self.schedule.add(self.commons)

    def required(self):
        # self.count = 0
        self.policies = Sequential(
            [
                SyncState(),
                CreateParticipant(),
                CreateProposal(),
                CreateFunding(),
                # Should update the sentiment here as well
                SyncState(),
                ProcessActiveProposals(),
                ParticipantVoting(),
                ProposalFunding(),
                # Add more sentiment here
                ParticipantSentiment(),
                SyncState(),
            ]
        )

    @property
    def participants(self) -> Iterable[Participant]:

        return []

    def bootstrap(self, params: CommonsConfig):
        self.run_time = params.run_time
        self.params = params
        self.schedule: BaseScheduler = RandomActivation(self)
        """Sets up the simulation variables, states, and agents."""

        return self.booter.bootload(params, self)

    def get_flags(self):
        return StepSpace()

    def start_step(self):
        pass
        # return super().start_step()

    def end_step(self):
        pass
        # return super().end_step()

    def step(self):
        # tell all the agents in the model to run their step function
        # Just resetiing a variable that needsd to be reset before processing
        # Collecting code
        # Collect data for the simulation using mesa's data collection code.
        # https://mesa.readthedocs.io/en/stable/tutorials/intro_tutorial.html#collecting-data

        self.state.conviction_proposals = []
        self.state.policy_log = {}
        # logger.debug(self.state)
        self.flags = self.get_flags()
        self.state = self.policies.transform(self.state)

        self.schedule.step()
        # Here we update the state of the model
        self.state.timestep = self.schedule.time

    def run_model(self):
        for i in range(self.run_time):
            self.step()


def main():
    pass


if __name__ == "__main__":
    main()
