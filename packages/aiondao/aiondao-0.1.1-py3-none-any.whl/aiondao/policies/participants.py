import copy
from typing import cast
from aiondao.libs.states import SimState

import numpy as np
from aiondao import config
from aiondao.agents.commons import TokenBatch
from aiondao.agents.members import Participant
from aiondao.utils.networking import (
    add_participant,
    find_in_edges_of_type_for_proposal,
    get_participants,
)
from auto_all import start_all
from aiondao.schemas import (
    InvestmentInput,
    PolicyAggregate,
    ParticipantPurchase,
)

from aiondao.libs.states import SimState
from aiondao._imports import *


# from aiondao.interfaces

start_all(globals())


class CreateNewParticipant:
    def __init__(self):
        self.agg = PolicyAggregate()

    def randomize(self, state: SimState):
        commons = state.commons
        fns = state.to_fns()
        sentiment = state.sentiment
        timestep = state.timestep

        speculation_days = state.confs.speculation_days
        multiplier_new_participants = state.confs.multiplier_new_participants

        dict_ans = {}
        if timestep < speculation_days:
            # If in speculation period, the arrival rate is higher
            arrival_rate = 0.5 + 0.5 * sentiment
            multiplier = multiplier_new_participants
            max_new_participants = config.max_new_participants * multiplier
        else:
            arrival_rate = (1 + sentiment) / config.arrival_rate_denominator
            max_new_participants = config.max_new_participants

        for _ in range(int(max_new_participants)):
            if fns.prob_fn(arrival_rate):
                # Here we randomly generate each participant's post-Hatch
                # investment, in DAI/USD.
                #
                # expon.rvs() arguments:
                #
                # loc is the minimum number, so if loc=100, there will be no
                # investments < 100
                #
                # scale is the standard deviation, so if scale=2, investments will
                # be around 0-12 DAI or even 15, if scale=100, the investments will be
                # around 0-600 DAI.
                participant_investment = fns.exp_fn(
                    loc=config.investment_new_participant_min,
                    scale=config.investment_new_participant_stdev,
                )
                tokens = commons.dai_to_tokens(participant_investment)

                self.agg.invests.append(
                    InvestmentInput(investment=participant_investment, tokens=tokens)
                )
        return dict_ans

    def su_add_to_network(self, state: SimState):

        network = state.network

        probability_func = state.confs.probability_func
        exponential_func = state.confs.exponential_func
        random_number_func = state.confs.random_number_func
        # speculation_days = state.confs.random_func
        # network = state.network
        # probability_func = params["probability_func"]
        # exponential_func = params["exponential_func"]
        random_number_func = state.confs.random_number_func
        params = {}
        for idx, invest in enumerate(self.agg.invests):
            if invest.is_valid():
                network, idx = add_participant(
                    network,
                    Participant(
                        holdings=TokenBatch(vesting=0, nonvesting=invest.tokens),
                        prob_fn=probability_func,  # type: ignore
                        random_number_func=random_number_func,  # type: ignore
                    ),
                    exponential_func,
                    random_number_func,
                )

                if params.get("debug", True):
                    print(
                        "GenerateNewParticipant: A new Participant {} invested {}DAI for {} tokens".format(
                            idx, invest.investment, invest.tokens
                        )
                    )
        state.network = network
        return "network", network

    def su_add_investment_to_commons(self, state: SimState):
        commons = state.commons
        for _, invest in enumerate(self.agg.invests):

            if invest.is_valid():
                commons.deposit(invest.investment)
        state.commons = commons
        return "commons", commons

    def su_update_participants_token_batch_age(self, state: SimState, **kwargs):
        network = state.network
        participants = get_participants(network)
        for pidx, participant in participants:
            participant = cast(Participant, participant)

            participant.update_token_batch_age()
        state.network = network
        return "network", network


class ParticipantBuysTokens:
    """
    When implementing buying tokens, Participants may either buy in bulk with no
    slippage, or endure slippage while buying. Neither is realistic but I'd say
    no slippage is closer to what Participants will experience in real life.

    When implementing selling tokens, slippage is more likely to change the
    decision. In any case, let us implement no slippage first since it is easier
    to reason with.

    Also, buying in bulk is easier to implement in cadCAD because if the state
    update function changes the Commons object each time a Participant buys
    in/sells out, then it would have to update the network and commons object in
    the same function, which is not allowed in cadCAD.
    """

    def p_decide_to_buy_tokens_bulk(self, state: SimState):
        network = state.network
        commons = state.commons
        participants = get_participants(network)
        ans = {}
        params = {}
        total_dai = 0

        for i, participant in participants:
            participant = cast(Participant, participant)
            # If a participant decides to buy, it will be specified in units of DAI.
            # If a participant decides to sell, it will be specified in units of tokens.
            x = participant.buy()
            if x > 0:
                total_dai += x
                ans[i] = x

        # Now that we have the sum of DAI, ask the Commons object how many
        # tokens this would be minted as a result. This will be inaccurate due
        # to slippage, and we need the result of this policy to be final to
        # avoid chaining 2 state update functions, so we run the deposit on a
        # throwaway copy of Commons
        if total_dai == 0:
            if params.get("debug", True):
                print(
                    "ParticipantBuysTokens: No Participants bought tokens in timestep {}".format(
                        state.timestep
                    )
                )
            return ParticipantPurchase(
                **{
                    "participant_decisions": ans,
                    "total_dai": 0,
                    "tokens": 0,
                    "token_price": 0,
                    "final_token_distribution": {},
                }
            )

        else:
            commons2 = copy.copy(commons)
            tokens, token_price = commons2.deposit(total_dai)

            final_token_distribution = {}
            for i in ans:
                final_token_distribution[i] = ans[i] / total_dai

            if params.get("debug", True):
                print(
                    "ParticipantBuysTokens: These Participants have decided to buy tokens with this amount of DAI: {}".format(
                        ans
                    )
                )
                print(
                    "ParticipantBuysTokens: A total of {} DAI will be deposited. {} tokens should be minted as a result at a price of {} DAI/token".format(
                        total_dai, tokens, token_price
                    )
                )

            return ParticipantPurchase(
                **{
                    "participant_decisions": ans,
                    "total_dai": total_dai,
                    "tokens": tokens,
                    "token_price": token_price,
                    "final_token_distribution": final_token_distribution,
                }
            )

    def su_buy_participants_tokens(
        self, state: SimState, agg: PolicyAggregate, **kwargs
    ):
        commons = state.commons
        purchase = agg.purchase
        if purchase is None:
            return
        if purchase.total_dai > 0:
            tokens, realized_price = commons.deposit(purchase.total_dai)
            if purchase.tokens != tokens or purchase.token_price != realized_price:
                raise Exception(
                    "ParticipantBuysTokens: {} tokens were minted at a price of {} (expected: {} with price {})".format(
                        tokens, realized_price, purchase.tokens, purchase.token_price
                    )
                )

        return "commons", commons

    def su_update_participants_tokens(
        self, state: SimState, agg: PolicyAggregate, **kwargs
    ):
        network = state.network
        purchase = agg.purchase
        if purchase is None:
            return
        decisions = purchase.participant_decisions
        final_token_distribution = purchase.final_token_distribution
        tokens = purchase.tokens

        for participant_idx, decision in decisions.items():
            network.nodes[participant_idx]["item"].increase_holdings(
                final_token_distribution[participant_idx] * tokens
            )

        return "network", network


class ParticipantSellsTokens:
    def __init__(self) -> None:
        self.agg = PolicyAggregate()

    def p_decide_to_sell_tokens_bulk(self, state: SimState, **kwargs):
        network = state.network
        commons = state.commons
        participants = get_participants(network)
        ans = {}
        total_tokens = 0
        for i, participant in participants:
            # If a participant decides to buy, it will be specified in units of DAI.
            # If a participant decides to sell, it will be specified in units of tokens.
            x = participant.sell()
            if x > 0:
                total_tokens += x
                ans[i] = x

        # Now that we have the sum of tokens, ask the Commons object how many
        # DAI would be redeemed as a result. This will be inaccurate due
        # to slippage, and we need the result of this policy to be final to
        # avoid chaining 2 state update functions, so we run the operation on a
        # throwaway copy of Commons
        if total_tokens == 0:
            if params.get("debug"):
                print(
                    "ParticipantSellsTokens: No Participants sold tokens in timestep {}".format(
                        step
                    )
                )
            return PolicyAggregate(
                **{
                    "participant_decisions": ans,
                    "total_tokens": 0,
                    "dai_returned": 0,
                    "realized_price": 0,
                }
            )
        else:
            commons2 = copy.copy(commons)
            dai_returned, realized_price = commons2.burn(total_tokens)

            final_dai_distribution = {}
            for i in ans:
                final_dai_distribution[i] = ans[i] / total_tokens

            if params.get("debug"):
                print(
                    "ParticipantSellsTokens: These Participants have decided to sell this many  tokens: {}".format(
                        ans
                    )
                )
                print(
                    "ParticipantSellsTokens: A total of {} tokens will be burned. {} DAI should be returned as a result, at a price of {} DAI/token".format(
                        total_tokens, dai_returned, realized_price
                    )
                )

            return PolicyAggregate(
                **{
                    "participant_decisions": ans,
                    "total_tokens": total_tokens,
                    "dai_returned": dai_returned,
                    "realized_price": realized_price,
                }
            )

    def su_burn_participants_tokens(
        self, state: SimState, agg: PolicyAggregate, **kwargs
    ):
        commons = state.commons
        self.agg.purchase
        if agg.total_tokens > 0:
            dai_returned, realized_price = commons.burn(agg.total_tokens)
            if agg.dai_returned != dai_returned or agg.realized_price != realized_price:
                raise Exception(
                    "ParticipantSellsTokens: {} DAI was returned at a price of {} (expected: {} with price {})".format(
                        dai_returned,
                        realized_price,
                        agg.dai_returned,
                        agg.realized_price,
                    )
                )

        return "commons", commons

    def su_update_participants_tokens(
        self, state: SimState, aggregate: PolicyAggregate, **kwargs
    ):
        network = state.network
        purchase = aggregate.purchase
        if purchase is None:
            return
        decisions = purchase.participant_decisions
        dai_returned = purchase.dai_returned

        for participant_idx, decision in decisions.items():
            network.nodes[participant_idx]["item"].spend(decision)

        return "network", network


class ParticipantExits:
    def p_participant_decides_if_he_wants_to_exit(
        self, state: SimState, aggregate: PolicyAggregate, **kwargs
    ):
        # A lot of these decisions can ge moved to individual participants
        params = {}
        network = state.network
        participants = get_participants(network)
        defectors = {}
        for i, participant in participants:
            participant = cast(Participant, participant)
            if participant.wants_to_exit():
                defectors[i] = {
                    "sentiment": participant.sentiment,
                    "holdings": participant.holdings.total,
                }

        if params.get("debug"):
            print(
                "ParticipantExits: Participants {} (2nd number is their sentiment) want to exit".format(
                    defectors
                )
            )
        return {"defectors": defectors}

    def su_remove_participants_from_network(self, state: SimState, **kwargs):
        # network = state.network
        network = state.network
        defectors = _input["defectors"]

        for i, _ in defectors.items():
            network.remove_node(i)

        return "network", network

    def su_burn_exiters_tokens(self, state: SimState, **kwargs):
        commons = state.commons
        network = state.network
        defectors = _input["defectors"]

        burnt_token_results = {}
        for i, v in defectors.items():
            dai_returned, realized_price = commons.burn(v["holdings"])
            burnt_token_results[i] = {
                "dai_returned": dai_returned,
                "realized_price": realized_price,
            }

        return "commons", commons

    def su_update_sentiment_when_proposal_becomes_active(
        self, state: SimState, **kwargs
    ):
        network = state.network
        policy_output_passthru = state.policy_output
        if not policy_output_passthru:
            return

        report = {}
        for idx in policy_output_passthru["proposal_idxs_with_enough_conviction"]:
            for participant_idx, proposal_idx, _ in find_in_edges_of_type_for_proposal(
                network, idx, "support"
            ):
                edge = network.edges[participant_idx, proposal_idx]
                if edge["support"].is_author:
                    sentiment_old = network.nodes[participant_idx]["item"].sentiment
                    sentiment_new = (
                        sentiment_old + config.sentiment_bonus_proposal_becomes_active
                    )
                    sentiment_new = 1 if sentiment_new > 1 else sentiment_new
                    network.nodes[participant_idx]["item"].sentiment = sentiment_new

                    report[participant_idx] = {
                        "proposal_idx": proposal_idx,
                        "sentiment_old": sentiment_old,
                        "sentiment_new": sentiment_new,
                    }

        if params.get("debug"):
            for i in report:
                print(
                    "ParticipantExits: Participant {} changed his sentiment from {} to {} because Proposal {} became active".format(
                        i,
                        report[i]["sentiment_old"],
                        report[i]["sentiment_new"],
                        report[i]["proposal_idx"],
                    )
                )
        return "network", network

    def su_update_sentiment_when_proposal_becomes_failed_or_completed(
        self, state: SimState, **kwargs
    ):
        network = state.network
        policy_output_passthru = s["policy_output"]

        proposal_status_delta = {
            "failed": config.sentiment_bonus_proposal_becomes_failed,
            "succeeded": config.sentiment_bonus_proposal_becomes_completed,
        }
        report = {}
        for status, delta in proposal_status_delta.items():
            for idx in policy_output_passthru[status]:
                for (
                    participant_idx,
                    proposal_idx,
                    _,
                ) in find_in_edges_of_type_for_proposal(network, idx, "support"):
                    edge = network.edges[participant_idx, proposal_idx]
                    # Update the participant sentiment if he/she is the proposal creator
                    # or if participant has staked on the proposal (tokens > 0)
                    if edge["support"].is_author or edge["support"].tokens > 0:
                        sentiment_old = network.nodes[participant_idx]["item"].sentiment
                        sentiment_new = sentiment_old + (
                            edge["support"].affinity * delta
                        )
                        sentiment_new = np.clip(sentiment_new, a_min=0.0, a_max=1.0)
                        network.nodes[participant_idx]["item"].sentiment = sentiment_new

                        report[participant_idx] = {
                            "proposal_idx": proposal_idx,
                            "sentiment_old": sentiment_old,
                            "sentiment_new": sentiment_new,
                            "status": status,
                        }

        if params.get("debug"):
            for i in report:
                print(
                    "ParticipantExits: Participant {} changed his sentiment from {} to {} because Proposal {} became {}".format(
                        i,
                        report[i]["sentiment_old"],
                        report[i]["sentiment_new"],
                        report[i]["proposal_idx"],
                        report[i]["status"],
                    )
                )
        return "network", network


class ParticipantSentiment:
    def su_update_sentiment_decay(self, state: SimState, **kwargs):
        network = state.network

        participants = get_participants(network)
        for participant_idx, participant in participants:
            sentiment_old = network.nodes[participant_idx]["item"].sentiment
            sentiment_new = sentiment_old - config.sentiment_decay
            sentiment_new = 0 if sentiment_new < 0 else sentiment_new
            network.nodes[participant_idx]["item"].sentiment = sentiment_new

        return "network", network
