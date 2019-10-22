import numpy as np
import rl.common.Constant as CNSTNT
from rl.common import policy, Tiling
from rl.control.BaseControl import BaseControl


class EpisodicSemiGradientSARSA(BaseControl):
    def __init__(self, env, discount_factor, exploration_rate, step_size, tiling: Tiling):
        assert isinstance(tiling, Tiling), 'tiling parameter is not Tiling object'

        super().__init__(env, discount_factor)
        self.exploration_rate = exploration_rate
        self.step_size = step_size
        self.weight = np.zeros((env.action_space, tiling.tile_size()))

    def run(self, number_of_episode):
        runs = {}
        for i in range(number_of_episode):
            state = self.env.reset()
            action = policy.epsilon_greedy(self.exploration_rate, self.action_space, self.Q[state, :])
            is_terminal = False
            while not is_terminal:
                state_next, reward, is_terminal, info = self.env.step(CNSTNT.ACTIONS_VALUES[action])
                action_next = policy.epsilon_greedy(self.exploration_rate, self.action_space, self.Q[state_next, :])
                self.Q[state, action] += self.step_size * (
                        reward + self.discount_factor * self.Q[state_next, action_next] - self.Q[state, action])
                state = state_next
                action = action_next
            total_length, total_reward, _ = self.env.history()
            runs[i] = (total_length, total_reward)
        self.PI = np.argmax(self.Q, axis=1)
        super().save_model()
        return runs
