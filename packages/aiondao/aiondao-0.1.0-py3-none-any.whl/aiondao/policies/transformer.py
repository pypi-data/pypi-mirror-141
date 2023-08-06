import numpy as np
from aiondao import config
from aiondao import utils as utilz
from typing import Optional
from aiondao.agents.commons import TokenBatch
from aiondao.interfaces.policy import IPolicyTransform
from aiondao.libs.states import SimState
from aiondao._imports import *
from aiondao.libs.conviction import trigger_threshold
from aiondao.schemas import InvestmentInput

from aiondao.utils.networking import (
    add_participant,
    add_proposal,
    calc_median_affinity,
    calc_total_conviction,
    calc_total_funds_requested,
    find_in_edges_of_type_for_proposal,
    get_edges_by_type,
    get_participants,
    get_proposals,
    get_proposals_by_participant_and_status,
)
from loguru import logger
from aiondao.utils.mixins import StateAccessors
from aiondao.agents.members import Participant, Proposal, ProposalStatus

from aiondao.utils.networking import (
    calc_median_affinity,
    calc_total_funds_requested,
    get_participants,
)
from loguru import logger


class ExamplePolicy(IPolicyTransform):
    def execute(self, state: SimState) -> Optional[SimState]:
        state.policy_log.append({"message": "ExamplePolicy"})
        return state


class SyncState(IPolicyTransform):
    def execute(self, state: SimState) -> Optional[SimState]:
        state.collateral_pool = state.commons._collateral_pool
        state.token_supply = state.commons.token_supply
        state.token_price = state.commons.token_price()
        state.funding_pool = state.commons.funding_pool
        return state


class IStatefulPolicyBlock(StateAccessors, IPolicyTransform, abc.ABC):
    @abc.abstractmethod
    def transform_steps(self, state: Optional[SimState] = None) -> Optional[SimState]:
        # Run the steps here independently and let the state self register
        return self.state

    def execute(self, state: SimState) -> Optional[SimState]:
        self.register_state(state)
        self.transform_steps()
        return self.state


class CreateParticipant(IStatefulPolicyBlock):
    def check_for_and_add_random_entrant(self):
        commons = self.state.commons
        fns = self.state.to_fns()
        sentiment = self.state.sentiment
        timestep = self.state.timestep

        speculation_days = self.state.confs.speculation_days
        multiplier_new_participants = self.state.confs.multiplier_new_participants
        investments = []
        if timestep < speculation_days:
            # If in speculation period, the arrival rate is higher
            arrival_rate = 0.5 + 0.5 * sentiment
            multiplier = multiplier_new_participants
            max_new_participants = config.max_new_participants * multiplier
        else:
            arrival_rate = (1 + sentiment) / config.arrival_rate_denominator
            max_new_participants = config.max_new_participants

        for _ in range(int(max_new_participants)):
            # logger.info((_, max_new_participants))
            if not self.prob_fn(arrival_rate):
                continue
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

            # Get token conversion
            tokens = commons.dai_to_tokens(participant_investment)

            invest = InvestmentInput(investment=participant_investment, tokens=tokens)
            investments.append(invest)
            if not invest.is_valid():
                continue

            """
                network, i = add_participant(network, Participant(TokenBatch(
                    0, ans["new_participant_tokens"]), probability_func,
                    random_number_func), exponential_func, random_number_func)

                if params.get("debug"):
                    print("GenerateNewParticipant: A new Participant {} invested {}DAI for {} tokens".format(
                        i, ans['new_participant_investment'], ans['new_participant_tokens']))
            
            """

            network, idx = add_participant(
                self.network,
                Participant(
                    holdings=TokenBatch(vesting=0, nonvesting=invest.tokens),
                    prob_fn=self.prob_fn,  # type: ignore
                    random_number_func=self.rand_fn,  # type: ignore
                ),
                self.exp_fn,
                self.rand_fn,
            )
            self.state.network = network

            self.commons.deposit(invest.investment)

    def update_token_batch_ages(self):
        network = self.state.network
        participants = get_participants(network)
        for _, participant in participants:
            participant = cast(Participant, participant)

            participant.update_token_batch_age()
        self.state.network = network

    def transform_steps(self, state: Optional[SimState] = None) -> Optional[SimState]:
        self.check_for_and_add_random_entrant()
        self.update_token_batch_ages()
        return super().transform_steps(state)


class CreateProposal(IStatefulPolicyBlock):
    def random_generate_proposal(self) -> Optional[SimState]:
        participants_dict = self.gx.parts.all_dict()
        # participants_dict = dict(participants)
        selected_idx = self.state.confs.choice_func(list(participants_dict.keys()))
        participant = participants_dict[selected_idx]

        wants_to_create_proposal = participant.create_proposal(
            calc_total_funds_requested(self.network),
            calc_median_affinity(self.network),
            self.state.funding_pool,
        )
        return wants_to_create_proposal, selected_idx

    def transform_steps(self, state: Optional[SimState] = None) -> Optional[SimState]:
        created_proposal, proposed_by = self.random_generate_proposal()
        if not created_proposal:
            return state
        rescale = self.funding_pool * config.scale_factor
        requested_funds = self.gamma_func(
            config.funds_requested_alpha,
            loc=config.funds_requested_min,
            scale=rescale,
        )
        proposal = Proposal(
            funds_requested=requested_funds,
            trigger=trigger_threshold(
                requested_funds,
                self.funding_pool,
                self.token_supply,
                self.cp.max_proposal_request,
            ),
        )
        network, _ = add_proposal(self.network, proposal, proposed_by, self.rand_fn)
        self.state.network = network


class CreateFunding(IStatefulPolicyBlock):
    def transform_steps(self, state: Optional[SimState] = None) -> Optional[SimState]:
        exits = [
            self.exp_fn(
                loc=config.speculator_position_size_min,
                scale=config.speculator_position_size_stdev,
            )
            for i in range(config.speculators)
        ]
        funding = sum(exits) * self.commons.exit_tribute
        self.commons._funding_pool += funding
        return self.state


class ProcessActiveProposals(IStatefulPolicyBlock):
    def determine_proposal_outcomes(self):
        probability_func = self.prob_fn

        active_proposals = get_proposals(self.network, status=ProposalStatus.ACTIVE)
        failed_procedures = []
        successul_procedures = []
        for idx, proposal in active_proposals:
            r_failure = 1 / (
                config.base_failure_rate + np.log(proposal.funds_requested)
            )
            r_success = 1 / (
                config.base_success_rate + np.log(proposal.funds_requested)
            )
            if probability_func(r_failure):
                failed_procedures.append(idx)
            elif probability_func(r_success):
                successul_procedures.append(idx)

        return failed_procedures, successul_procedures

    def update_proposal_statuses(self):
        failed, success = self.determine_proposal_outcomes()
        self.state.policy_output["failed"] = failed
        self.state.policy_output["success"] = success
        for idx in failed:
            self.network.nodes[idx]["item"].status = ProposalStatus.FAILED

        for idx in success:
            self.network.nodes[idx]["item"].status = ProposalStatus.COMPLETED

        return self.state

    def transform_steps(self, state: Optional[SimState] = None) -> Optional[SimState]:
        self.update_proposal_statuses()
        return self.state


class ParticipantVoting(IStatefulPolicyBlock):
    # Get voite participantion
    def get_participant_votes(self):
        """
        p_participant_votes_on_proposal_according_to_affinity
        # We generate the probability of voting on a proposal according to the affinity to the proposal.
        This policy collects data from the DiGraph to tell the Participant class
        which candidate proposals it supports, and
        Participant.vote_on_candidate_proposals() will decide which proposals it
        will take action on.

        Then, Participant.stake_across_all_supported_proposals() will tell us
        how much it will stake on each of them.
        """
        participants = get_participants(self.network)

        participants_stakes = {}
        for participant_idx, participant in participants:
            proposal_idx_affinity = {}  # {4: 0.9, 5: 0.9}
            candidate_proposals = get_proposals_by_participant_and_status(
                self.network,
                participant_idx=participant_idx,
                status_filter=[ProposalStatus.CANDIDATE],
            )
            for proposal_idx, proposal in candidate_proposals.items():
                proposal_idx_affinity[proposal_idx] = proposal["support"].affinity
            proposals_that_participant_cares_enough_to_vote_on = (
                participant.vote_on_candidate_proposals(proposal_idx_affinity)
            )

            stake_across_all_supported_proposals_input = []
            for (
                proposal_idx,
                affinity,
            ) in proposals_that_participant_cares_enough_to_vote_on.items():
                stake_across_all_supported_proposals_input.append(
                    (affinity, proposal_idx)
                )
            stakes = participant.stake_across_all_supported_proposals(
                stake_across_all_supported_proposals_input
            )

            participants_stakes[participant_idx] = stakes

            # if params.get("debug"):
            # if proposals_that_participant_cares_enough_to_vote_on:
            #     logger.warning(
            #         f"ParticipantVoting: Participant {participant_idx} was given Proposals with corresponding affinities {proposal_idx_affinity} and he decided to vote on {proposals_that_participant_cares_enough_to_vote_on}, distributing his tokens thusly {stakes}"
            #     )
        return participants_stakes

    def update_participants_votes(self):
        """
        Simply update the support edges with the new amount of tokens the
        Participant has staked on the Proposal. Leave the conviction calculation
        to another state update function.
        """
        network = self.network

        for participant_idx, v in self.get_participant_votes().items():

            for proposal_idx, tokens_staked in v.items():
                # I assume there is no longer a need to recalculate a la
                # https://github.com/randomshinichi/conviction/blob/9d1bc9513475dc30d33e3232b385234d0295d361/conviction_system_logic3.py#L510
                # because the tokens were already distributed proportionally to
                # the affinities in
                # p_participant_votes_on_proposal_according_to_affinity()
                # Also, do not recalculate conviction here. Leave that to ProposalFunding.su_calculate_conviction()
                start_support = network[participant_idx][proposal_idx]["support"]
                start_support.tokens = tokens_staked
                network[participant_idx][proposal_idx]["support"] = start_support

        self.state.network = network
        return self.state

    def transform_steps(self, state: Optional[SimState] = None) -> Optional[SimState]:
        self.get_participant_votes()
        return self.update_participants_votes()


class ProposalFunding(IStatefulPolicyBlock):
    """Determine if there are any proposals that should go on to get fundint.

    If there are, then determine how much funding should be requested.
    """

    def find_approved_proposals(self):
        """
        This policy simply goes through the Proposals to see if their thresholds
        are smaller than their gathered conviction. If the conviction is higher, then pass the proposals to be activated.
        """

        proposals_w_enough_conviction = []
        proposals = get_proposals(self.network, status=ProposalStatus.CANDIDATE)
        for idx, proposal in proposals:
            total_conviction = calc_total_conviction(self.network, idx)
            proposal.conviction = total_conviction
            is_above_threshold = proposal.has_enough_conviction(
                self.funding_pool, self.token_supply, self.capt.max_proposal_request
            )

            if is_above_threshold:
                proposals_w_enough_conviction.append(idx)

        return proposals_w_enough_conviction

    def process_activated_proposals(self):
        active_proposals = self.find_approved_proposals()
        self.state.conviction_proposals = active_proposals
        for idx in active_proposals:
            self.network.nodes[idx]["item"].status = ProposalStatus.ACTIVE
            funds = self.network.nodes[idx]["item"].funds_requested
            self.commons.spend(funds)
        return self.state

    def update_age_and_conviction_thresholds(self):

        proposals = get_proposals(self.network, status=ProposalStatus.CANDIDATE)
        for _, proposal in proposals:
            proposal.update_age()
            proposal.update_threshold(
                self.funding_pool,
                self.token_supply,
                max_proposal_request=self.capt.max_proposal_request,
            )

        return self.state

    def recalculate_convictions(self):
        """
        Actually calculates the conviction. This function should only run ONCE
        per timestep/iteration!
        """
        alpha = self.cp.days_to_80p_of_max_voting_weight

        support_edges = get_edges_by_type(self.network, "support")
        for i, j in support_edges:
            proposal_status = self.network.nodes[j]["item"].status
            if proposal_status == ProposalStatus.CANDIDATE:
                edge = self.network.edges[i, j]
                prior_conviction = edge["support"].conviction
                current_tokens = edge["support"].tokens
                local_support = edge["support"]
                local_support.conviction = current_tokens + alpha * prior_conviction
                edge["support"] = local_support
                self.network.edges[i, j]["support"] = edge["support"]

        return self.state

    def transform_steps(self, state: Optional[SimState] = None) -> Optional[SimState]:
        self.process_activated_proposals()
        self.update_age_and_conviction_thresholds()
        self.recalculate_convictions()

        return self.state


class ParticipantSentiment(IStatefulPolicyBlock):
    def transform_steps(self, state: Optional[SimState] = None) -> Optional[SimState]:
        participants = get_participants(self.state.network)
        for participant_idx, participant in participants:
            sentiment_old = self.state.network.nodes[participant_idx]["item"].sentiment
            sentiment_new = sentiment_old - config.sentiment_decay
            sentiment_new = 0 if sentiment_new < 0 else sentiment_new
            self.state.network.nodes[participant_idx]["item"].sentiment = sentiment_new

        return super().transform_steps(self.state)

    # def execute(self, state: SimState) -> Optional[SimState]:
    #     logger.debug("Create new participant")
    #     state.collateral_pool = state.commons._collateral_pool
    #     state.token_supply = state.commons.token_supply
    #     state.token_price = state.commons.token_price()
    #     state.funding_pool = state.commons.funding_pool
    #     return state
