from typing import List, Optional, Tuple, Union
from aiondao._imports import *
from aiondao.agents.members import Participant, Proposal, ProposalStatus
from aiondao.utils.networking import (
    add_proposal,
    get_participants,
    get_proposals,
    calc_total_funds_requested,
    calc_total_funds_requested,
    add_participant,
    calc_median_affinity,
    calc_total_conviction,
    calc_total_affinity,
    calc_avg_sentiment,
)


import networkx as nx
import toolz as tlz


class _BaseModel(RelaxedModel):
    class Config:
        arbitrary_types_allowed = True


# Proposals and Participants queries. To be accessed by `GraphORM` class decorators parts and props`
class ProposalsQuery(BaseModel):
    net: nx.DiGraph

    def all(self, status: Optional[ProposalStatus] = None) -> List[Participant]:
        return list(dict(get_proposals(self.net, status)).values())

    def add(
        self, proposal: Proposal, proposed_by: int, random_number_func
    ) -> Tuple[nx.DiGraph, int]:
        return add_proposal(self.net, proposal, proposed_by, random_number_func)

    def by_parts_and_type(self, participant: Participant, type: str) -> List[Proposal]:
        return []

    def by_parts_and_stats(self, participant: Participant, type: str) -> List[Proposal]:
        return []

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


class ParticipantsQuery(_BaseModel):
    net: nx.DiGraph

    def all(self) -> List[Proposal]:
        return list(dict(get_participants(self.net)).values())

    def all_dict(self) -> Dict[int, Proposal]:
        return dict(get_participants(self.net))

    def add(
        self, participant: Participant, exponential_func, random_number_func
    ) -> Tuple[nx.DiGraph, int]:
        return add_participant(
            self.net, participant, exponential_func, random_number_func
        )

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


# A dataclass for graph orm with property functions for 'participants' and 'proposals'
class GraphORM(BaseModel):

    net: nx.DiGraph

    @property
    def parts(self) -> ParticipantsQuery:
        return ParticipantsQuery(net=self.net)

    @property
    def props(self) -> ProposalsQuery:
        return ProposalsQuery(net=self.net)

    @property
    def total_funds_requested(self) -> float:
        """The total_funds_requested property."""
        return calc_total_funds_requested(self.net)

    @property
    def median_affinity(self) -> float:
        """The total_funds_requested property."""
        return calc_median_affinity(self.net)

    @property
    def total_conviction(self) -> float:
        """The total_funds_requested property."""
        return calc_total_conviction(self.net, 0)

    @property
    def total_affinity(self) -> float:
        """The total_funds_requested property."""
        return calc_total_affinity(self.net)

    @property
    def avg_sentiment(self) -> float:
        """The total_funds_requested property."""
        return calc_avg_sentiment(self.net)

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow
