import abc
from mesa.time import BaseScheduler


class IEconomy(abc.ABC):
    @abc.abstractmethod
    def step(self):
        pass

    @abc.abstractmethod
    def start_step(self):
        pass

    @abc.abstractmethod
    def end_step(self):
        pass
