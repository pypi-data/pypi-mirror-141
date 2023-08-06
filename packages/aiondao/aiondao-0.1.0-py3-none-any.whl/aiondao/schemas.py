from aiondao._imports import *
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class InvestmentInput(RelaxedModel):
    investment: float
    tokens: float

    def is_valid(self):
        return True if self.investment > 0 and self.tokens > 0 else False


class ParticipantPurchase(SyncModel):
    participant_decisions: List[InvestmentInput]
    total_dai: float
    tokens: float
    token_price: float
    final_token_distribution: Dict[str, Any] = {}
    dai_returned: float = 0
    realized_price: float = 0


class PurchaseEvent(BaseModel):
    participant_decisions: List[InvestmentInput]
    total_dai: float
    tokens: float
    token_price: float
    final_token_distribution: Dict[str, Any] = {}
    dai_returned: float = 0
    realized_price: float = 0


class Defector(RelaxedModel):
    sentiment: float = 0.75
    holdings: float


class PolicyAggregate(RelaxedModel):
    invests: List[InvestmentInput] = []
    purchase: Optional[ParticipantPurchase] = None
    decision: Optional[ParticipantPurchase] = None
    total_tokens: float = 0
    dai_returned: float = 0
    realized_price: float = 0
    defectors: Dict[str, Defector] = {}
