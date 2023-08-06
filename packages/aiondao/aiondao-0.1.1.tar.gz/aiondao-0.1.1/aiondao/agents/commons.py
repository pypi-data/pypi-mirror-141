from aiondao._imports import *
from loguru import logger

from typing import List, Optional, Tuple

from mesa import Agent, Model
from aiondao.libs.abcurve import AugmentedBondingCurve

from aiondao import config
from pydantic import Extra, root_validator

from aiondao.interfaces.models import IEconomy

ilog = logger.info


def vesting_curve(day: int, cliff_days: int, halflife_days: float) -> float:
    """
    The vesting curve includes the flat cliff, and the halflife curve where tokens are gradually unlocked.
    It looks like _/--
    """
    return 1 - config.vesting_curve_halflife ** ((day - cliff_days) / halflife_days)


def convert_80p_to_cliff_and_halflife(
    days: int, v_ratio: int = 2
) -> Tuple[float, float]:
    """
    For user's convenience, we ask him after how many days he would like 80% of his tokens to be unlocked.
    This needs to be converted into a half life (unit days).
    2.321928094887362 is log(base0.5) 0.2, or log 0.2 / log 0.5.
    v_ratio is cliff / halflife, and its default is determined by Commons Stack
    """
    halflife_days = days / (config.log_base05_of_02 + v_ratio)
    cliff_days = v_ratio * halflife_days
    return cliff_days, halflife_days


def hatch_raise_split_pools(total_hatch_raise, hatch_tribute) -> Tuple[float, float]:
    """Splits the hatch raise between the funding / collateral pool based on the fraction."""
    funding_pool = hatch_tribute * total_hatch_raise
    collateral_pool = total_hatch_raise * (1 - hatch_tribute)
    return funding_pool, collateral_pool


@dataclass(config=autovalid, order=True)
class VestingOptions:
    cliff_days: int
    halflife_days: int


@dataclass(config=autovalid)
class TokenBatch:
    vesting: float
    nonvesting: float
    vesting_spent: float = 0.0
    age_days: int = 0

    vesting_options: Optional[VestingOptions] = None

    def __post_init__(self):
        self.vesting_options = cast(VestingOptions, self.vesting_options)
        self.cliff_days = (
            0 if not self.vesting_options else self.vesting_options.cliff_days  # type: ignore
        )
        self.halflife_days = (
            0 if not self.vesting_options else self.vesting_options.halflife_days  # type: ignore
        )

    @property
    def total(self) -> float:
        return (self.vesting - self.vesting_spent) + self.nonvesting

    def __bool__(self):
        if self.total > 0:
            return True
        return False

    def __add__(self, other):
        total_vesting = self.vesting + other.vesting
        total_nonvesting = self.nonvesting + other.nonvesting
        return total_vesting, total_nonvesting

    def __sub__(self, other):
        total_vesting = self.vesting - other.vesting
        total_nonvesting = self.nonvesting - other.nonvesting
        return total_vesting, total_nonvesting

    def update_age(self, iterations: int = 1):
        """
        Adds the number of iterations to TokenBatch.age_days
        """
        self.age_days += iterations
        return self.age_days

    def unlocked_fraction(self) -> float:
        """
        returns what fraction of the TokenBatch is unlocked to date
        """
        if self.cliff_days and self.halflife_days:
            u = vesting_curve(self.age_days, self.cliff_days, self.halflife_days)
            return u if u > 0 else 0
        else:
            return 1.0

    def spend(self, x: float):
        """
        checks if you can spend so many tokens, then decreases this TokenBatch
        instance's value accordingly
        """
        if x > self.spendable():
            raise Exception(
                "Not so many tokens are available for you to spend yet ({})".format(
                    self.age_days
                )
            )

        y = x - self.nonvesting
        if y > 0:
            self.vesting_spent += y
            self.nonvesting = 0.0
        else:
            self.nonvesting = abs(y)

        return self.vesting, self.vesting_spent, self.nonvesting

    def spendable(self) -> float:
        """
        spendable() = (self.unlocked_fraction * self.vesting - self.vesting_spent) + self.nonvesting
        Needed in case some Tokens were burnt before.
        """
        return (
            (self.unlocked_fraction() * self.vesting) - self.vesting_spent
        ) + self.nonvesting


def create_token_batches(
    hatcher_contributions: List[float],
    desired_token_price: float,
    cliff_days: float,
    halflife_days: float,
) -> Tuple[List[TokenBatch], float]:
    """
    hatcher_contributions: a list of hatcher contributions in DAI/ETH/whatever
    desired_token_price: used to determine the initial token supply
    vesting_80p_unlocked: vesting parameter - the number of days after which 80% of tokens will be unlocked, including the cliff period
    """
    total_hatch_raise = sum(hatcher_contributions)
    initialtoken_supply = total_hatch_raise / desired_token_price

    # In the hatch, everyone buys in at the same time, with the same price. So just split the token supply amongst the hatchers proportionally to their contributions
    tokens_per_hatcher = [
        (x / total_hatch_raise) * initialtoken_supply for x in hatcher_contributions
    ]

    token_batches = [
        TokenBatch(x, 0, vesting_options=VestingOptions(cliff_days, halflife_days))
        for x in tokens_per_hatcher
    ]
    return token_batches, initialtoken_supply


class CommonAgent(Agent, IEconomy):
    def __init__(
        self,
        unique_id: int,
        model: Model,
        total_hatch_raise: float,
        token_supply: float,
        *args,
        hatch_tribute: float = 0.2,
        exit_tribute: float = 0,
        kappa: int = 2,
        hatch_tokens: Optional[float] = None,
        _funding_pool: Optional[float] = None,
        _collateral_pool: Optional[float] = None,
        bonding_curve: Optional[AugmentedBondingCurve] = None,
        **kwargs,
    ) -> None:
        super().__init__(unique_id, model, *args, **kwargs)

        self.total_hatch_raise = total_hatch_raise
        self.token_supply = token_supply
        self.hatch_tribute = hatch_tribute
        self.exit_tribute = exit_tribute
        self.kappa = kappa
        self.hatch_tokens = hatch_tokens

        self._collateral_pool = (1 - self.hatch_tribute) * self.total_hatch_raise
        self._funding_pool = (
            self.hatch_tribute * self.total_hatch_raise
        )  # 0.35 * total_hatch_raise = 35%

        # hatch_tokens keeps track of the number of tokens that were created when hatching, so we can calculate the unlocking of those
        self.hatch_tokens = self.token_supply
        self.bonding_curve = AugmentedBondingCurve(
            reserve=self._collateral_pool,
            supply=self.token_supply,
            kappa=self.kappa,
        )

        # Options
        self.exit_tribute = self.exit_tribute

    def __repr__(self) -> str:
        return f"Commons(collateral={self.collateral_pool}, funding={self.funding_pool}, tokens={self.token_supply})"

    @property
    def funding_pool(self) -> float:
        """The funding_pool property."""
        return self._funding_pool

    @funding_pool.setter
    def funding_pool(self, value: Union[float, int]):
        self._funding_pool = value

    @property
    def collateral_pool(self) -> float:
        """The collateral_pool property."""
        return self._collateral_pool

    @collateral_pool.setter
    def collateral_pool(self, value: float):
        self._collateral_pool = value

    @property
    def _token_supply(self) -> float:
        """The _token_supply property."""
        return self.token_supply

    @_token_supply.setter
    def _token_supply(self, value: float):
        self.token_supply = value

    def deposit(self, dai):
        """
        Deposit DAI after the hatch phase. This means all the incoming deposit goes to the collateral pool.
        """
        tokens, realized_price = self.bonding_curve.deposit(
            dai, self._collateral_pool, self.token_supply
        )
        self.token_supply += tokens
        self._collateral_pool += dai
        return tokens, realized_price

    def burn(self, tokens):
        """
        Burn tokens, with/without an exit tribute.
        """
        dai, realized_price = self.bonding_curve.burn(
            tokens, self._collateral_pool, self.token_supply
        )
        self.token_supply -= tokens
        self._collateral_pool -= dai
        money_returned = dai

        if self.exit_tribute:
            self._funding_pool += self.exit_tribute * dai
            money_returned = (1 - self.exit_tribute) * dai
        return money_returned, realized_price

    def dai_to_tokens(self, dai):
        """
        Given the size of the common's collateral pool, return how many tokens would x DAI buy you.
        """
        price = self.bonding_curve.get_token_price(self._collateral_pool)
        return dai / price

    def token_price(self):
        """
        Query the bonding curve for the current token price, given the size of the commons's collateral pool.
        """
        return self.bonding_curve.get_token_price(self._collateral_pool)

    def spend(self, amount):
        """
        Decreases the Common's funding_pool by amount.
        Raises an exception if this would make the funding pool negative.
        """
        if self._funding_pool - amount < 0:
            raise Exception(
                "{} funds requested but funding pool only has {}".format(
                    amount, self._funding_pool
                )
            )
        self._funding_pool -= amount
        return

    def start_step(self):
        pass
        # return super().start_step()

    def end_step(self):
        pass

    def step(self) -> None:

        return super().step()


class LooseWrapper(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


class Common(LooseWrapper):
    # All of these are to be calculated at a later time.
    total_hatch_raise: float
    token_supply: float
    hatch_tribute: float = 0.2
    exit_tribute: float = 0.0
    kappa: float = 2

    hatch_tokens: Optional[float] = None
    _funding_pool: Optional[float] = None
    _collateral_pool: Optional[float] = None
    # bonding_curve: AugmentedBondingCurve

    @root_validator
    def validate_commons(cls, values):
        logger.warning("Validating commons")
        values["_collateral_pool"] = (1 - values["hatch_tribute"]) * values[
            "total_hatch_raise"
        ]
        values["_funding_pool"] = (
            values["hatch_tribute"] * values["total_hatch_raise"]
        )  # 0.35 * total_hatch_raise = 35%

        kappa = values.get("kappa", 2)
        collateral = values["_collateral_pool"]
        supply = values["token_supply"]

        logger.info((kappa, collateral, supply))
        # hatch_tokens keeps track of the number of tokens that were created when hatching, so we can calculate the unlocking of those
        # values["hatch_tokens"] = values["token_supply"]
        values["bonding_curve"] = AugmentedBondingCurve(
            reserve=collateral,
            supply=supply,
            kappa=kappa,
        )

        # Options
        values["exit_tribute"] = values.get("exit_tribute", 0.2)

        return values

    @property
    def _token_supply(self) -> float:
        """The _token_supply property."""
        return self.token_supply

    @_token_supply.setter
    def _token_supply(self, value: float):
        self.token_supply = value

    @property
    def collateral_pool(self) -> float:
        """The collateral_pool property."""
        if self._collateral_pool is not None:
            return self._collateral_pool
        self._collateral_pool = (1 - self.hatch_tribute) * self.total_hatch_raise
        return self._collateral_pool

    @collateral_pool.setter
    def collateral_pool(self, value: float):
        self._collateral_pool = value

    def deposit(self, dai):
        """
        Deposit DAI after the hatch phase. This means all the incoming deposit goes to the collateral pool.
        """
        tokens, realized_price = self.bonding_curve.deposit(
            dai, self.collateral_pool, self.token_supply
        )
        self.token_supply += tokens
        self._collateral_pool += dai
        return tokens, realized_price

    def burn(self, tokens):
        """
        Burn tokens, with/without an exit tribute.
        """

        dai, realized_price = self.bonding_curve.burn(
            tokens, self.collateral_pool, self.token_supply
        )
        self.token_supply -= tokens
        self._collateral_pool -= dai
        money_returned = dai

        if self.exit_tribute:
            self._funding_pool += self.exit_tribute * dai
            money_returned = (1 - self.exit_tribute) * dai
        return money_returned, realized_price

    def dai_to_tokens(self, dai):
        """
        Given the size of the common's collateral pool, return how many tokens would x DAI buy you.
        """
        price = self.bonding_curve.get_token_price(self.collateral_pool)
        return dai / price

    def token_price(self):
        """
        Query the bonding curve for the current token price, given the size of the commons's collateral pool.
        """
        return self.bonding_curve.get_token_price(self.collateral_pool)

    def spend(self, amount):
        """
        Decreases the Common's funding_pool by amount.
        Raises an exception if this would make the funding pool negative.
        """
        if self._funding_pool - amount < 0:
            raise Exception(
                "{} funds requested but funding pool only has {}".format(
                    amount, self._funding_pool
                )
            )
        self._funding_pool -= amount
        return

    def step(self) -> None:
        return super().step()

    # def update_bond(self):
    #     self.bonding_curve.reserve = self._collateral_pool

    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow


#
Commons = Common


def main():
    pass


if __name__ == "__main__":
    main()
