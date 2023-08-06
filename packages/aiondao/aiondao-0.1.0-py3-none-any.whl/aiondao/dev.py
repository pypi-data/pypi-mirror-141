from aiondao._imports import *
from aiondao.economy import AionEconomy
from aiondao.libs.states import CommonsConfig


def run_dev():
    logger.info("----- Starting AionDAO DEV -----")
    conf = CommonsConfig()
    economy = AionEconomy(conf)

    # model = economy
    for i in range(20):
        economy.step()


if __name__ == "__main__":
    run_dev()
