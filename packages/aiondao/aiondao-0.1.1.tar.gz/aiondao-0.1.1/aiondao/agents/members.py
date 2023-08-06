import copy

# from aiondao.utils import networking as netty
from dataclasses import dataclass as dataclassog
from enum import Enum, auto
from typing import Callable, List, Optional, Tuple, Union

import numpy as np
from aiondao import config
from aiondao._imports import *
from aiondao.agents.commons import TokenBatch
from aiondao.interfaces.models import IEconomy
from aiondao.libs.conviction import trigger_threshold
from aiondao.libs.states import SimState
from aiondao.schemas import Defector
from aiondao.utils._utilz import attrs
from mesa import Agent, Model

RandomNumCallable = Callable[..., float]
RandomNumCallable = Callable

# from aiondao.libs.graph import GraphORM
CHANGE_DELTA = {
    "failed": config.sentiment_bonus_proposal_becomes_failed,
    "success": config.sentiment_bonus_proposal_becomes_completed,
}


class StateAccessors:
    def __init__(self) -> None:
        self.__state = None

    # Properties to access network, functinf pool, and graphorm queries
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: SimState):
        self.__state = state

    @property
    def network(self):
        return self.__state.network

    @property
    def capt(self):
        return self.__state.confs

    @property
    def cp(self):
        return self.__state.confs

    @property
    def commons(self):
        return self.__state.commons

    @property
    def gx(self):
        return GraphORM(net=self.__state.network)

    @property
    def funding_pool(self):
        return self.__state.funding_pool

    @property
    def funding_pool(self):
        return self.__state.token_supply

    @property
    def gamma_func(self):
        return self.__state.confs.gamma_func

    @property
    def participants(self):
        return self.gx.parts.all()

    @property
    def proposals(self):
        return self.gx.props.all()

    @property
    def exp_fn(self):
        return self.__state.confs.exponential_func

    @property
    def prob_fn(self):
        return self.__state.confs.exponential_func

    def register_state(self, state: SimState):
        self.state = state


class ProposalStatus(Enum):
    CANDIDATE = auto()
    ACTIVE = auto()
    COMPLETED = auto()
    FAILED = auto()


class ParticipantSupport(SyncModel):
    affinity: float
    tokens: float = 0.0
    conviction: float = 0.0
    is_author: bool = False


# candidate: proposal is being evaluated by the commons
# active: has been approved and is funded
# completed: the proposal was effective/successful
# failed: did not get to active status or failed after funding


@dataclass(config=autovalid)
class Proposal:
    # Fields that are required
    funds_requested: int
    trigger: float

    conviction = 0
    status = ProposalStatus.CANDIDATE
    age = 0

    def update_age(self):
        self.age += 1
        return self.age

    def update_threshold(
        self, funding_pool: float, token_supply: float, max_proposal_request: float
    ):
        if self.status == ProposalStatus.CANDIDATE:
            self.trigger = trigger_threshold(
                self.funds_requested, funding_pool, token_supply, max_proposal_request
            )
        else:
            self.trigger = np.nan
        return self.trigger

    def has_enough_conviction(
        self, funding_pool: float, token_supply: float, max_proposal_request
    ):
        """
        It's just a conviction < threshold check, but we recalculate the
        trigger_threshold so that the programmer doesn't have to remember to run
        update_threshold before running this method.
        """
        if self.status == ProposalStatus.CANDIDATE:
            threshold = trigger_threshold(
                self.funds_requested, funding_pool, token_supply, max_proposal_request
            )
            if self.conviction < threshold:
                return False
            return True
        else:
            raise (
                Exception(
                    "Proposal is not a Candidate Proposal and so asking it if it will pass is inappropriate"
                )
            )


class ParticipantDecision(StateAccessors):
    def __init__(self, participant: "Participant") -> None:
        super().__init__()
        self.participant = participant
        # self.__state: Optional[SimState] = None

    @property
    def model(self):
        return self.participant.model

    # @property
    # def net(self):
    #     """The net property."""
    #     if self.__state is None:
    #         raise AttributeError("State space was not found.")  # type: ignore
    #     return self.__state.network

    @property
    def commons(self):
        """The net property."""
        if self.__state is None:
            raise AttributeError("State space was not found.")  # type: ignore
        return self.__state.commons

    def is_state(self) -> bool:
        return True if self.__state else False

    def reset(self, state: SimState, params: Dict[str, Any] = {}):
        self.aggregate = 0.0
        self.__state = state

    """Processing Buy Decisions"""

    def decide_buy(self) -> Tuple[bool, float]:
        buy_amount = self.participant.buy()
        return bool(buy_amount), buy_amount

    def process_buy(self):
        is_buy, total_dai = self.decide_buy()
        commons2 = copy.copy(self.commons)
        if not is_buy:
            return
        # Calculate the amount minted that'll likely be minted
        estimated_tokens, estimated_token_price = commons2.deposit(total_dai)
        if not bool(total_dai):
            return

        minted_tokens, realized_price = self.commons.deposit(total_dai)
        if estimated_tokens != minted_tokens or estimated_token_price != realized_price:
            raise Exception(
                "ParticipantBuysTokens: {} tokens were minted at a price of {} (expected: {} with price {})".format(
                    minted_tokens,
                    realized_price,
                    estimated_tokens,
                    estimated_token_price,
                )
            )
        self.participant.increase_holdings(minted_tokens)

    """Processing Sell Decisions"""

    def decide_sell(self) -> Tuple[bool, float]:
        sell_amount = self.participant.sell()
        return bool(sell_amount), sell_amount

    def estimate_sale(self, tokens_sold: float):
        commons2 = copy.copy(self.commons)
        # Calculate the amount minted that'll likely be minted
        return commons2.burn(tokens_sold)

    def process_sell(self):
        is_buy, tokens_sold = self.decide_sell()
        if not is_buy:
            return

        # Estimate the remaining price and and dai returned
        estimated_dai, estimated_price = self.estimate_sale(tokens_sold)

        if not bool(tokens_sold):
            logger.info("ParticipantSellsTokens: did not sell tokens")
            return

        dai_returned, realized_price = self.commons.burn(tokens_sold)
        if dai_returned != estimated_dai or estimated_price != realized_price:
            raise Exception(
                "ParticipantSellsTokens: {} tokens were minted at a price of {} (expected: {} with price {})".format(
                    tokens_sold,
                    dai_returned,
                    realized_price,
                )
            )
        self.participant.spend(tokens_sold)

    """Dealing with Participant Exits"""

    def participant_decides_exit(self) -> bool:
        if not self.participant.wants_to_exit():
            return False
        return True

    # Function to get participants sentiment and holdings
    def get_participant_info(self) -> Dict[str, Any]:
        return Defector(
            sentiment=self.participant.sentiment,
            holdings=self.participant.holdings.total,
        )

    def burn_exiters_tokens(self, exiter_holdings: float):
        dai_returned, realized_price = self.commons.burn(exiter_holdings)

    def process_exit_logic(self):
        if not self.participant_decides_exit():
            # logger.info(
            #     f"Participant {self.participant.unique_id} does not want to exit"
            # )
            return
        logger.error(f"Participant {self.participant.unique_id} wants to exit")
        defect = self.get_participant_info()
        self.network.remove_node(self.participant.unique_id)
        self.participant.has_existed = True
        self.burn_exiters_tokens(defect.holdings)

    def get_proposals(self, status_types: List[ProposalStatus] = []) -> List[Proposal]:
        from aiondao.utils.networking import get_proposals_by_participant_and_status

        if not status_types:
            # Get all of the status types
            status_types = [
                ProposalStatus.ACTIVE,
                ProposalStatus.CANDIDATE,
                ProposalStatus.COMPLETED,
                ProposalStatus.FAILED,
            ]
        return get_proposals_by_participant_and_status(
            self.net, self.participant.unique_id, status_filter=status_types
        )

    def update_sentiment_conviction(self):
        logger.info(f"Updating active sentiment for {self.participant.unique_id}")
        convictions = self.state.conviction_proposals

        for prop_id in convictions:
            edge = self.network.edges[self.participant.unique_id, prop_id]
            if not "support" in edge:
                continue
            edge_support = edge["support"]
            if not edge_support.is_author:
                continue
            part = self.participant
            s1 = part.sentiment
            sentiment = np.clip(
                s1 + config.sentiment_bonus_proposal_becomes_active,
                a_min=0.0,
                a_max=1.0,
            )
            self.participant.sentiment = sentiment

    def update_sentiment_success_fail(self):
        logger.success(
            f"Updating success/fail sentiment for {self.participant.unique_id}"
        )
        for status, proposal_idxs in self.state.policy_output.items():
            if not proposal_idxs:
                continue
            for proposal_idx in proposal_idxs:
                edge = self.network.edges[self.participant.unique_id, proposal_idx]
                if not "support" in edge:
                    continue

                supporter = edge["support"]
                if not (supporter.is_author or supporter.tokens > 0):
                    continue

                logger.warning(supporter)
                s1 = self.participant.sentiment
                sentiment = np.clip(
                    s1 + (supporter.affinity * CHANGE_DELTA[status]),
                    a_min=0.0,
                    a_max=1.0,
                )
                self.participant.sentiment = sentiment

    def process_sentiment(self):
        # Go through proposal logic and update sentiment
        self.update_sentiment_conviction()
        self.update_sentiment_success_fail()
        # for idx in policy_output_passthru["proposal_idxs_with_enough_conviction"]:
        # self.participant.sentiment = self.participant.sentiment_update()


# @dataclass


class Participant(BorgIdModel, Agent):
    holdings: TokenBatch = None
    prob_fn: Callable = None
    random_number_func: Callable = None
    model: Optional[Union["Model", IEconomy]] = None
    unique_id: Optional[int] = None
    sentiment: float = 0
    has_existed: bool = False
    __step_logic: ParticipantDecision = None

    def __post_init__(self):
        self.prob_fn = self.prob_fn
        self._random_number_func = self.random_number_func

        self.sentiment = self._random_number_func()

    @property
    def logic(self) -> ParticipantDecision:
        if self.__step_logic is None:
            self.__step_logic = ParticipantDecision(self)
        return self.__step_logic

    @property
    def flags(self):
        return self.model.flags

    def buy(self) -> float:
        """
        If the Participant decides to buy more tokens, returns the number of
        tokens. Otherwise, return 0.

        This method does not modify itself, it simply returns the answer so that
        cadCAD's state update functions will make the changes and maintain its
        functional-ness.
        """
        engagement_rate = config.engagement_rate_multiplier_buy * self.sentiment
        force = self.sentiment - config.sentiment_sensitivity
        if self.prob_fn(engagement_rate) and force > 0:
            delta_holdings = (
                self.random_number_func() * force * config.delta_holdings_scale
            )
            return delta_holdings
        return 0

    def sell(self) -> float:
        """
        Decides to sell some tokens, and if so how many. If the Participant
        decides to sell some tokens, returns the number of tokens. Otherwise,
        return 0.

        This method does not modify itself, it simply returns the answer so that
        cadCAD's state update functions will make the changes and maintain its
        functional-ness.
        """
        engagement_rate = config.engagement_rate_multiplier_sell * self.sentiment
        force = self.sentiment - config.sentiment_sensitivity
        if self.prob_fn(engagement_rate) and force < 0:
            spendable = self.holdings.spendable()
            # It is expected that the function returns a positive value for the
            # amount sold.
            force = -1 * force
            delta_holdings = self.random_number_func() * force * spendable
            return delta_holdings
        return 0

    def increase_holdings(self, x: float):
        """
        increase_holdings() is the opposite of spend() and adds to the
        nonvesting part of the TokenBatch.
        """
        self.holdings.nonvesting += x
        return (
            self.holdings.vesting,
            self.holdings.vesting_spent,
            self.holdings.nonvesting,
        )

    def spend(self, x: float) -> Tuple[float, float, float]:
        """
        Participant.spend() is simply a front to TokenBatch.spend().
        """
        return self.holdings.spend(x)

    def create_proposal(
        self, total_funds_requested, median_affinity, funding_pool
    ) -> bool:
        """
        Here the Participant will decide whether or not to create a new
        Proposal.

        This equation, originally from randomly_gen_new_proposal(), is a
        systems-type simulation. An individual Participant would likely think in
        a different way, and thus this equation should change. Nevertheless for
        simplicity's sake, we use this same equation for now.

        Explanation: If the median affinity is high, the Proposal Rate should be
        high.

        If total funds_requested in candidate proposals is much lower than the
        funding pool (i.e. the Commons has lots of spare money), then people are
        just going to pour in more Proposals.
        """
        percent_of_funding_pool_being_requested = total_funds_requested / funding_pool
        proposal_rate = median_affinity / (1 + percent_of_funding_pool_being_requested)
        new_proposal = self.prob_fn(proposal_rate)
        return new_proposal

    def vote_on_candidate_proposals(self, candidate_proposals: dict) -> dict:
        """
        Here the Participant decides which Candidate Proposals he will stake
        tokens on. This method does not decide how many tokens he will stake
        on them, because another function should decide how the tokens should be
        balanced across the newly supported proposals and the ones the
        Participant already supported.

        Copied from
        participants_buy_more_if_they_feel_good_and_vote_for_proposals()

        candidate dict format:
        {
            proposal_idx: affinity,
            ...
        }

        NOTE: the original cadCAD policy returned {'delta_holdings':
        delta_holdings, 'proposals_supported': proposals_supported}
        proposals_supported seems to include proposals ALREADY supported by the
        participant, but I don't think it is needed.
        """
        new_voted_proposals = {}
        engagement_rate = 1.0
        if self.prob_fn(engagement_rate):
            # Put your tokens on your favourite Proposals, where favourite is
            # calculated as 0.75 * (the affinity for the Proposal you like the
            # most) e.g. if there are 2 Proposals that you have affinity 0.8,
            # 0.9, then 0.75*0.9 = 0.675, so you will end up voting for both of
            # these Proposals
            #
            # A Zargham work of art.
            for candidate in candidate_proposals:
                affinity = candidate_proposals[candidate]
                # Hardcoded 0.75 instead of a configurable sentiment_sensitivity
                # because modifying sentiment_sensitivity without changing the
                # hardcoded cutoff value of 0.5 may cause unintended behaviour.
                # Also, 0.75 is a reasonable number in this case.
                cutoff = config.candidate_proposals_cutoff * np.max(
                    list(candidate_proposals.values())
                )
                if cutoff < 0.5:
                    cutoff = 0.5

                if affinity > cutoff:
                    new_voted_proposals[candidate] = affinity

        return new_voted_proposals

    def stake_across_all_supported_proposals(
        self, supported_proposals: List[Tuple[float, int]]
    ) -> dict:
        """
        Rebalances the Participant's tokens across the (possibly updated) list of Proposals
        supported by this Participant.

        These tokens can come from a Participant's vesting and nonvesting TokenBatches.

        supported_proposals format:
        [(affinity, proposal_idx)...]
        """
        tokens_per_supported_proposal = {}
        supported_proposals = sorted(supported_proposals, key=lambda tup: tup[0])

        affinity_total = sum([a for a, idx in supported_proposals])
        for affinity, proposal_idx in supported_proposals:
            tokens_per_supported_proposal[proposal_idx] = self.holdings.total * (
                affinity / affinity_total
            )

        return tokens_per_supported_proposal

    def wants_to_exit(self):
        """
        Returns True if the Participant wants to exit (if sentiment < 0.5,
        random chance of exiting) and if the Participant has no vesting
        token, otherwise False.
        """
        sensitivity_exit = config.sentiment_sensitivity_exit
        vesting = self.holdings.vesting

        if self.sentiment < sensitivity_exit and vesting == 0:
            engagement_rate = config.engagement_rate_multiplier_exit * self.sentiment
            return self.prob_fn(1 - engagement_rate)
        return False

    def update_token_batch_age(self):
        """
        Participant.update_token_batch_age() is simply a front to
        TokenBatch.update_age().
        """
        return self.holdings.update_age()

    def step(self):
        # self.logic.reset(self.state)
        self.logic.register_state(self.model.state)
        # self.logic.reset(self.state)
        # ! Update Token Holdings if you haven't already
        self.logic.process_buy()
        self.logic.process_sell()
        self.logic.process_exit_logic()
        self.logic.process_sentiment()
        # is_buy, amount = self.logic.decide_buy()
        # debug((is_buy, amount))
        return super().step()
