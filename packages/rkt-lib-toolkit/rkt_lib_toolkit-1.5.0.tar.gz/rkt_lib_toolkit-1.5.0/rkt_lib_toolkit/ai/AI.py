from typing import List, Optional

import numpy as np
import pandas as pd
from pandas import DataFrame

from rkt_lib_toolkit.logger import Logger
from rkt_lib_toolkit.config import Config


class QLearning:

    def __init__(self,
                 actions: List,
                 should_load: bool = False,
                 qtable_file_to_load: str = "",
                 alpha: float = 0.1,
                 gamma: float = 0.5):

        self._me = self.__class__.__name__
        self._logger: Logger = Logger(caller_class=self.me)
        self._logger.set_logger(caller_class=self.me, output="stream")
        self._config: Config = Config()

        self.learning_rate: float = alpha
        self.discount_factor: float = gamma

        self.qtable: Optional['DataFrame'] = None
        self.available_actions = actions
        self.previous_state: str = "start"
        self.previous_action: str = "do-nothing"

        self.load(should_load, qtable_file_to_load)

    # PROPERTIES
    @property
    def me(self) -> str:
        return self._me

    @me.setter
    def me(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_me' property must be a string")
        self._me: str = value

    @property
    def logger(self) -> Logger:
        return self._logger

    @logger.setter
    def logger(self, value: Logger) -> None:
        if not isinstance(value, Logger):
            raise TypeError("The '_logger' property must be a 'Logger'")
        self._logger: Logger = value

    @property
    def config(self) -> Config:
        return self._config

    @config.setter
    def config(self, value: Config) -> None:
        if not isinstance(value, Config):
            raise TypeError("The '_config' property must be a 'Config'")
        self._config: Config = value

    @property
    def learning_rate(self) -> float:
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("The '_learning_rate' property must be a float")
        self._learning_rate: float = value

    @property
    def discount_factor(self) -> float:
        return self._discount_factor

    @discount_factor.setter
    def discount_factor(self, value: float) -> None:
        if not isinstance(value, float):
            raise TypeError("The '_discount_factor' property must be a float")
        self._discount_factor: float = value

    @property
    def qtable(self) -> 'DataFrame':
        return self._qtable

    @qtable.setter
    def qtable(self, value: 'DataFrame') -> None:
        if not isinstance(value, DataFrame) and value is not None:
            raise TypeError("The '_qtable' property must be a DataFrame")
        self._qtable: Optional['DataFrame'] = value

    @property
    def previous_state(self) -> str:
        return self._previous_state

    @previous_state.setter
    def previous_state(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_previous_state' property must be a string")
        self._previous_state: str = value

    @property
    def previous_action(self) -> str:
        return self._previous_action

    @previous_action.setter
    def previous_action(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError("The '_previous_action' property must be a string")
        self._previous_action: str = value

    @property
    def available_actions(self) -> List:
        return self._available_actions

    @available_actions.setter
    def available_actions(self, value: List) -> None:
        if not isinstance(value, List):
            raise TypeError("The '_available_actions' property must be a list")
        self._available_actions: List = value

    def __repr__(self) -> str:
        return f"QLearning(alpha={self.learning_rate}, gamma={self.discount_factor})"

    # Functions
    # # Management
    def save(self, file: str) -> None:
        self.qtable.to_pickle(file)

    def load(self, do_load: bool, file_to_load: str) -> None:
        if do_load:
            self.qtable = pd.read_pickle(file_to_load)
        else:
            self.qtable = pd.DataFrame(columns=self.available_actions, dtype=np.float64)

    # # AI
    def choose_action(self, state: str, e_greedy=0.5):
        """
        Epsilon parameter is related to the epsilon-greedy (e_greedy) action selection procedure in the
        Q-learning algorithm.
        In the action selection step, we select the specific action based on the Q-values we already have.
        The epsilon parameter introduces randomness into the algorithm, forcing us to try different actions.
        This helps not to get stuck in a local optimum.

        If epsilon is set to 0, we never explore but always exploit the knowledge we already have.
        On the contrary, having the epsilon set to 1 force the algorithm to always take random actions and
        never use past knowledge. Usually, epsilon is selected as a small number close to 0.

        :param state:
        :param e_greedy:
        :return:
        """
        self.check_state_exist(state)
        if np.random.uniform() < e_greedy:
            action = np.random.choice(self.available_actions)
        else:
            state_action = self.qtable.loc[state, :]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index)
        return action

    def learn(self, state: str, action, reward: float) -> None:
        """
        Run for each step from 'BotAI'
        Original function is (pseudo-code: https://www.baeldung.com/cs/epsilon-greedy-q-learning):
        Q(S, A) <- Q(S, A) + alpha * [R + gamma * max(Q(S', A')) - Q(S, A)]
        where:
            Q: qtable
            S: State
            A: selected Action (see choose_action function)
            alpha: learning rate
            R: Reward
            gamma: discount factor
            S': previous State
            A': previous Action
            max: function max like np.max()

        :param state:
        :param action:
        :param reward:
        :return:
        """
        if self.previous_state != "start":
            self.check_state_exist(state)
            estimation_future_reward = self.qtable.loc[self.previous_state, self.previous_action]
            estimation_reward = self.qtable.loc[state, action]
            delta = self.learning_rate * (reward + self.discount_factor * estimation_future_reward - estimation_reward)
            self.qtable.loc[state, action] += delta
        self.previous_state = state
        self.previous_action = action

    def check_state_exist(self, state: str):
        if state not in self.qtable.index:
            self.qtable = self.qtable.append(pd.Series([0] * len(self.available_actions),
                                                       index=self.qtable.columns,
                                                       name=state))
