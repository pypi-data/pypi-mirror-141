from pydantic import BaseConfig, Extra

# Participant Sentiment Parameters
sentiment_decay: float = 0.005
sentiment_sensitivity: float = 0.75
candidate_proposals_cutoff: float = 0.75
delta_holdings_scale: float = 70000
sentiment_bonus_proposal_becomes_active: float = 0.5
sentiment_bonus_proposal_becomes_completed: float = 0.3
sentiment_bonus_proposal_becomes_failed: float = -0.1
engagement_rate_multiplier_buy: float = 0.6
engagement_rate_multiplier_sell: float = 0.6
engagement_rate_multiplier_exit: float = 0.3
sentiment_sensitivity_exit: float = 0.5

# Participant Investment Parameters
investment_new_participant_min: float = 0.0
investment_new_participant_stdev: float = 100

# Speculator Parameters
speculator_position_size_min: float = 200  # DAI
speculator_position_size_stdev: float = 200
speculators: int = 5

# Proposal Parameters
min_age_days: int = 2
scale_factor: float = 0.01
base_failure_rate: float = 0.15
base_success_rate: float = 0.30
funds_requested_alpha: int = 3
funds_requested_min: float = 0.001

# Trigger threshold Parameters
rho_multiplier: float = 0.5
rho_power: float = 2

# Vesting curve Parameters
vesting_curve_halflife: float = 0.5
log_base05_of_02: float = 2.321928094887362

# GenerateNewParticipant Parameters
arrival_rate_denominator: float = 10
max_new_participants: int = 1


class BroadConfig(BaseConfig):
    arbitrary_types_allowed = True


class cfgall(BroadConfig):

    extra = Extra.allow


class cfgign(BroadConfig):
    extra = Extra.ignore


class autovalid(BroadConfig):
    """Automatically validate assigned values."""

    extra = Extra.allow
    validate_assignment = True


class iautovalid(BroadConfig):
    """Automatically validate assigned values. with ignore extra."""

    extra = Extra.ignore
    validate_assignment = True
