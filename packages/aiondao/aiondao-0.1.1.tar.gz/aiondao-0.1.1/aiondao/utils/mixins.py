from aiondao.libs.states import SimState
from aiondao.libs.graph import GraphORM


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
    def token_supply(self):
        return self.__state.commons.token_supply

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
        return self.__state.confs.probability_func

    @property
    def rand_fn(self):
        return self.__state.confs.random_number_func

    def register_state(self, state: SimState):
        self.state = state
