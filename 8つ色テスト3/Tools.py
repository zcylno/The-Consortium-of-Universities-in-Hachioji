from collections import deque
import random
import torch
import numpy as np

import matplotlib.pyplot as plt


class Memory_Replay:
    def __init__(self, memory_size):
        self.memory = deque(maxlen=memory_size)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 经验存储
    def memory_push(self, s, a, r, s_):
        self.memory.append((s, a, r, s_))

    # 经验批量提取
    def memory_sample(self, sample_size):
        batch = []
        size = min(self.memory_len(), sample_size)
        batch = random.sample(self.memory, size)

        s = torch.cat([arr[0] for arr in batch])
        a = torch.cat([arr[1] for arr in batch])
        r = torch.FloatTensor([arr[2] for arr in batch])
        s_ = torch.cat([arr[3] for arr in batch])

        return s.to(self.device), a.to(self.device), r.to(self.device), s_.to(self.device)

    # 返回已存入经验的长度
    def memory_len(self):
        return len(self.memory)

    def memory_nobatch(self):
        memory_1 = random.sample(self.memory, 1)
        # print(memory_1)
        s = memory_1[0][0]
        a = memory_1[0][1]
        r = memory_1[0][2]
        s_ = memory_1[0][3]
        return s, a, r, s_


class OU_Noise:
    def __init__(self, action_dimension, mu=1, theta=0.15, sigma=0.2):
        self.action_dimension = action_dimension

        self.mu = mu

        self.theta = theta

        self.sigma = sigma

        self.state = np.ones(self.action_dimension) * self.mu

    def reset(self):
        self.state = np.ones(self.action_dimension) * self.mu

    def noise(self):
        x = self.state

        dx = self.theta * (self.mu - x) + self.sigma * np.random.randn(len(x))

        self.state = x + dx

        return self.state


def soft_update(target, online, tau):
    for target_param, online_param in zip(target.parameters(), online.parameters()):
        target_param.data.copy_(
            target_param.data * (1.0 - tau) + online_param.data * tau
        )


def hard_update(target, online):
    for target_param, param in zip(target.parameters(), online.parameters()):
        target_param.data.copy_(param.data)


def plot(count, data1, data2, data3, data4, data5, data6, data7, data8):
    plt.figure(2)
    plt.clf()
    plt.xlabel('times')
    plt.ylabel('cash_count')
    plt.plot(count,data1,color='#646464', label='color1')
    plt.plot(count,data2,color='green', label='color2')
    plt.plot(count,data3,color='black', label='color3')
    plt.plot(count,data4,color='blue', label='color4')
    plt.plot(count, data5, color='red', label='color5')
    plt.plot(count, data6, color='#969696', label='color6')
    plt.plot(count, data7, color='#fafafa', label='color7')
    plt.plot(count, data8, color='#c8c8c8', label='color8')
    plt.legend()  # 显示图例
    name = count[0]
    plt.savefig('images/' + str(name))
    plt.show()


def plt_img(img, name=None, save=None):
    from matplotlib import image
    plt.imshow(img.cpu().squeeze(0).permute(1, 2, 0).numpy(), interpolation='none')
    plt.title('Example extracted screen')
    if save is not None:
        img = img.cpu().squeeze(0).permute(1, 2, 0).numpy()

        image.imsave('images_color/' + name, img)
    # plt.show()


