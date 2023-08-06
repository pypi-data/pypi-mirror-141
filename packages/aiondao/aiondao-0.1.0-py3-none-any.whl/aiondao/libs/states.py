import random
from typing import Any, Callable, Dict, List, Optional
from aiondao._imports import *
from dataclasses_json import config


import networkx as nx

from aiondao.utils._utilz import (
    new_probability_func,
    new_exponential_func,
    new_gamma_func,
    new_random_number_func,
    new_choice_func,
)

from aiondao.agents.commons import (
    CommonAgent as CommonDAO,
    convert_80p_to_cliff_and_halflife,
)


class CommonsConfig(BaseModel):
    """
    There are just so many options that passing them via kwargs has become
    rather unwieldy. Also it would be useful to have some footnotes next to each
    parameter.

    Inject this paramter into class to control simulation parameters.
    """

    #
    hatch_tribute: float = 0.2
    exit_tribute: float = 0.35
    proposals: int = 2
    hatchers: int = 5
    kappa: int = 2
    vesting_80p_unlocked: int = 120
    days_to_80p_of_max_voting_weight: int = 10
    # maximum fraction of the funding pool that a proposal can ever request
    max_proposal_request: float = 0.2
    timesteps_days: int = 730
    random_seed: Optional[None] = Field(None)
    rand_seed: Optional[Callable] = None
    probability_func: Optional[Callable] = None
    exponential_func: Optional[Callable] = None
    gamma_func: Optional[Callable] = None
    random_number_func: Optional[Callable] = None
    choice_func: Optional[Callable] = None
    run_time: int = 20
    speculation_days: int = 120
    multiplier_new_participants: float = 0.2

    @root_validator
    def calculate_numerical_functions(cls, values):
        rand_seed = values.get("random_seed", None)
        probability_func = new_probability_func(rand_seed)
        exponential_func = new_exponential_func(rand_seed)
        gamma_func = new_gamma_func(rand_seed)
        random_number_func = new_random_number_func(rand_seed)
        choice_func = new_choice_func(rand_seed)

        values["probability_func"] = probability_func
        values["exponential_func"] = exponential_func
        values["gamma_func"] = gamma_func
        values["random_number_func"] = random_number_func
        values["choice_func"] = choice_func

        vest_unlocked_80 = values.get("vesting_80p_unlocked", 120)

        values["speculation_days"] = int(0.2 * vest_unlocked_80) + int(
            0.6 * vest_unlocked_80 * random_number_func()
        )
        values["multiplier_new_participants"] = 1 + int(9 * random_number_func())

        return values

    def alpha(self) -> float:
        """
        Converts days_to_80p_of_max_voting_weight to alpha.
        alpha = (1 - 0.8) ^ (1/t)
        """
        return 0.2 ** (1 / self.days_to_80p_of_max_voting_weight)

    def cliff_and_halflife(self) -> Tuple[float, float]:
        """
        This is just a wrapper around hatch.convert_80p_to_cliff_and_halflife().
        It is used here instead for logical consistency (having all derived
        configuration variables come from CommonsSimulationConfiguration), but
        defined in hatch for local consistency (having all hatch-related code in
        one place). Time will tell if this really matters.
        """
        return convert_80p_to_cliff_and_halflife(self.vesting_80p_unlocked)


class SimulationCalls:
    def __init__(self, state: "SimState") -> None:
        self.state = state

    def prob_fn(self, prob: float) -> float:
        return self.state.confs.probability_func(prob)  # type: ignore

    def exp_fn(self, loc: float, scale: float) -> float:
        return self.state.confs.exponential_func(loc=loc, scale=scale)  # type: ignore


class SimState(BorgModel):

    unique_id: int
    network: nx.DiGraph
    commons: CommonDAO
    funding_pool: float
    collateral_pool: float
    token_supply: float
    token_price: float
    policy_output: Optional[Dict[str, Any]] = {}
    sentiment: float = 0.75
    policy_log: List[Dict[str, Any]] = []
    timestep: Union[float, int] = 0
    testing_adder: int = 0
    confs: CommonsConfig = None
    conviction_proposals: List[Any] = []

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    def to_fns(self) -> SimulationCalls:
        return SimulationCalls(self)


class StepSpace(BorgModel):

    update_holdings_msg: bool = False
    crazy_id: int = 444
    # network: nx.DiGraph
    # commons: CommonDAO
    # funding_pool: float
    # collateral_pool: float
    # token_supply: float
    # token_price: float
    # policy_output: Optional[Dict[str, Any]] = None
    # sentiment: float = 0.75
    # policy_log: List[Dict[str, Any]] = []
    # timestep: Union[float, int] = 0
    # testing_adder: int = 0
    # confs: CommonsConfig = None

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    # def to_fns(self) -> SimulationCalls:
    #     return SimulationCalls(self)


"""

initial_conditions = {
            "network": network,
            "commons": commons,
            "funding_pool": commons._funding_pool,
            "collateral_pool": commons._collateral_pool,
            "token_supply": commons._token_supply,
            "token_price": commons.token_price(),
            "policy_output": None,
            "sentiment": 0.75,
        }
"""
