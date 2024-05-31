import matplotlib.pyplot as plt
import numpy as np
import gym
from matplotlib import animation
from IPython.display import HTML


class MazeEnv(gym.Env):
    def __init__(self) -> None:
        self.state = 0

        self.theta_0 = np.asarray(
            [[np.nan, 1, 1, np.nan],     # s0
             [np.nan, 1, np.nan, 1],      # s1
             [np.nan, np.nan, 1, 1],      # s2
             [1, np.nan, np.nan, np.nan], # s3 
             [np.nan, 1, 1, np.nan],      # s4
             [1, np.nan, np.nan, 1],      # s5
             [np.nan, 1, np.nan, np.nan], # s6 
             [1, 1, np.nan, 1]]           # s7
        )
        pass

    def reset(self):
        self.state = 0
        return self.state
    
    def step(self, action):
        if action == 0:
            self.state -= 3
        elif action == 1:
            self.state += 1
        elif action == 2:
            self.state += 3
        elif action == 3:
            self.state -= 1
        done = False
        reward = 0
        if self.state == 8:
            done = True
            reward = 1
        # state, reward, done, _
        return self.state, reward, done, {}
        
    def draw_maze(self):
        self.fig = plt.figure(figsize=(5, 5))
        ax = plt.gca()
        ax.set_xlim(0, 3)
        ax.set_ylim(0, 3)

        # 绘制迷宫边界
        boundary_points = [
            ([2, 3], [1, 1]),
            ([0, 1], [1, 1]),
            ([1, 1], [1, 2]),
            ([1, 2], [2, 2])
        ]
        for x, y in boundary_points:
            plt.plot(x, y, color='red', linewidth=2)

        # 设置文本样式
        text_style = dict(size=14, ha='center')

        # 定义状态位置和文本
        state_positions = [
            (0.5, 2.5, 'S0'),
            (1.5, 2.5, 'S1'),
            (2.5, 2.5, 'S2'),
            (0.5, 1.5, 'S3'),
            (1.5, 1.5, 'S4'),
            (2.5, 1.5, 'S5'),
            (0.5, 0.5, 'S6'),
            (1.5, 0.5, 'S7'),
            (2.5, 0.5, 'S8')
        ]
        special_texts = [
            (0.5, 2.3, 'START'),
            (2.5, 0.3, 'GOAL')
        ]

        # 绘制状态文本和特殊文本
        for x, y, text in state_positions + special_texts:
            plt.text(x, y, text, **text_style)

        # 绘制起点标记
        start_position = (0.5, 2.5)
        self.line, = ax.plot(start_position[0], start_position[1], marker='o', color='g', markersize=60)

        # 隐藏坐标轴
        plt.tick_params(axis='both', which='both', bottom=False, top=False, right=False, left=False,
                        labelbottom=False, labelleft=False)

        plt.show()

    def draw_videos(self, s_a_history):
        self.s_a_history = s_a_history
        def init():
            self.line.set_data([], [])
            return (self.line, )
        
        def animate(i):
            state = self.s_a_history[i][0]
            x = (state % 3)+0.5
            y = 2.5 - int(state/3)
            self.line.set_data(x, y)

        anim = animation.FuncAnimation(self.fig, animate, init_func=init, frames=len(s_a_history), interval=200, repeat=False)

        return HTML(anim.to_jshtml())
    