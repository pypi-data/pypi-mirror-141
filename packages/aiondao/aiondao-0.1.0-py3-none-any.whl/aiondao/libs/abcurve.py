from typing import Any
from pydantic import Extra
from pydantic.dataclasses import dataclass
from aiondao._imports import *


# value function for a given state (reserve,supply)
def invariant(reserve: float, supply: float, kappa: float):
    return (supply**kappa) / reserve


# value function for a given state (R,S)
def invariant(reserve: float, supply: float, power_invariant: float):

    return (supply**power_invariant) / reserve


# given a value function (parameterized by kappa)
# and an invariant coefficient invariant
# return Supply supply as a function of reserve


def supply(reserve: float, kappa: float, invariant: float):
    return (invariant * reserve) ** (1 / kappa)


# given a value function (parameterized by kappa)
# and an invariant coeficient invariant
# return a spot price P as a function of reserve


def spot_price(reserve: float, kappa: float, invariant: float):
    return kappa * reserve ** ((kappa - 1) / kappa) / invariant ** (1 / kappa)


# for a given state (reserve,supply)
# given a value function (parameterized by kappa)
# and an invariant coeficient invariant
# deposit d_reserve to Mint d_supply
# with realized price d_reserve/d_supply


def mint(
    d_reserve: float, reserve: float, supply: float, kappa: float, invariant: float
):
    d_supply = (invariant * (reserve + d_reserve)) ** (1 / kappa) - supply
    realized_price = d_reserve / d_supply
    return d_supply, realized_price


# for a given state (reserve,supply)
# given a value function (parameterized by kappa)
# and an invariant coeficient invariant
# burn d_supply to Withdraw d_reserve
# with realized price d_reserve/d_supply


def withdraw(
    d_supply: float, reserve: float, supply: float, kappa: float, invariant: float
):
    d_reserve = reserve - ((supply - d_supply) ** kappa) / invariant
    realized_price = d_reserve / d_supply
    return d_reserve, realized_price


class AugmentedBondingCurve(BaseModel):
    """Create a stateless bonding curve.

    reserve_initial (DAI)
    token_supply_initial (DAI)
    kappa (the exponent part of the curve, default is 2)
    """

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow
        validate_assignment = True

    reserve: float
    supply: float
    kappa: float
    invariant: Optional[float] = None
    _has_init: bool = PrivateAttr(False)

    @root_validator
    def calc_invariant(cls, values):
        reserve = values.get("reserve")
        supply = values.get("supply")
        kappa = values.get("kappa")
        values["invariant"] = invariant(
            reserve=reserve, supply=supply, power_invariant=kappa
        )
        return values

    # def __post_init__(self):
    #     self.invariant = invariant(self.reserve, self.supply, self.kappa)

    # def __repr__(self):
    #     return su

    def deposit(self, dai: float, current_reserve: float, current_token_supply: float):
        # Returns number of new tokens minted, and their realized price
        tokens, realized_price = mint(
            dai, current_reserve, current_token_supply, self.kappa, self.invariant
        )
        return tokens, realized_price

    def burn(
        self,
        tokens_millions: float,
        current_reserve: float,
        current_token_supply: float,
    ):
        # Returns number of DAI that will be returned (excluding exit tribute) when the user burns their tokens, with their realized price
        dai, realized_price = withdraw(
            tokens_millions,
            current_reserve,
            current_token_supply,
            self.kappa,
            cast(float, self.invariant),
        )
        return dai, realized_price

    def get_token_price(self, current_reserve: float):
        return spot_price(current_reserve, self.kappa, self.invariant)

    def get_token_supply(self, current_reserve: float):
        return supply(current_reserve, self.kappa, self.invariant)

    def update(self, reserve: float, supply: float):
        self.init_reserve = reserve
        self.supply = supply
