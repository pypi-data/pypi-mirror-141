from typing import List
from aiondao._imports import *
from aiondao.agents.members import Participant

# isort: on
import random
from aiondao.interfaces.models import IEconomy

# from aiondao.agents.dummy import DummyAgent
from aiondao.agents.commons import (
    CommonAgent,
    create_token_batches,
)

from aiondao.utils.networking import bootstrap_network
from aiondao.libs.states import CommonsConfig, SimState
from aiondao.libs.graph import GraphORM
import networkx as nx


class BootstrapSimulation:
    """Start everything necessary to run the simulation"""

    def get_graph(self, gx: nx.DiGraph):
        return GraphORM(net=gx)

    def bootload(self, confs: CommonsConfig, economy: "IEconomy"):
        state: SimState = self.create_state(confs, economy)
        self.register_participants(state, economy)
        return state

    def register_participants(self, state: SimState, economy: "IEconomy"):
        gx = self.get_graph(state.network)
        participants = gx.parts.all_dict()
        # base_id = random.randint(1200000, 1500000)
        for idx, part in participants.items():
            part.crazy_id = idx + 10001
            part.model = economy
            part.unique_id = idx
            part.logic.reset(state)
            # part.unique_id
            economy.schedule.add(part)
        return economy

    def create_state(self, confs: CommonsConfig, economy: "IEconomy"):
        contributions = [
            confs.random_number_func() * 10e5 for i in range(confs.hatchers)
        ]
        cliff_days, halflife_days = confs.cliff_and_halflife()
        token_batches, initial_token_supply = create_token_batches(
            contributions, 0.1, cliff_days, halflife_days
        )
        anchor_id = random.randint(10000, 12000)
        commons = CommonAgent(
            unique_id=anchor_id,
            model=economy,
            total_hatch_raise=sum(contributions),
            token_supply=initial_token_supply,
            hatch_tribute=confs.hatch_tribute,
            exit_tribute=confs.exit_tribute,
            kappa=confs.kappa,
        )

        # economy.schedule.add(commons)
        network = bootstrap_network(
            token_batches,
            confs.proposals,
            commons._funding_pool,
            commons._token_supply,
            confs.max_proposal_request,
            confs.probability_func,
            confs.random_number_func,
            confs.gamma_func,
            confs.exponential_func,
        )

        return SimState(
            unique_id=anchor_id,
            network=network,
            commons=commons,
            funding_pool=commons._funding_pool,
            collateral_pool=commons._collateral_pool,
            token_supply=commons._token_supply,
            token_price=commons.token_price(),
            policy_output={},
            sentiment=0.75,
            confs=confs,
        )
