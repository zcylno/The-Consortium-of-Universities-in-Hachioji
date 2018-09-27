import torch
import torch.nn as nn
import Net
import Tools
import random
import math


BATCH_SIZE = 128

LR = 0.001
GAMMA = 0.99
TAU = 0.001
TARGET_COUNT = 10
MEMORY_SIZE = 2000
EPS_START = 1
EPS_END = 0.08
EPS_DECAY = 10000000
SEED = 1
torch.cuda.manual_seed(SEED)


class Train:

    def __init__(self, action_dim):

        self.count = 0

        self.action_dim = action_dim


        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.memory = Tools.Memory_Replay(MEMORY_SIZE)

        self.online = Net.Net(self.action_dim).to(self.device)

        self.target = Net.Net(self.action_dim).to(self.device)

        self.optimizer = torch.optim.Adam(self.online.parameters(), LR)

        self.loss_func = nn.SmoothL1Loss()
        self.steps_done = 0
        #self.eps_threshold = 0


    def get_action(self,state):

        sample = random.random()
        eps_threshold = EPS_END + (EPS_START - EPS_END) * math.exp(-1. * self.steps_done / EPS_DECAY)
        #print(self.steps_done, eps_threshold)
        self.steps_done += 1
        if sample > 0.2:#eps_threshold:
            with torch.no_grad():
                return self.online(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(4)]], device=self.device, dtype=torch.long)

    def optimize(self):

        self.count += 1
        if self.count % TARGET_COUNT == 0:
            print("#######################update########################")
            Tools.soft_update(self.target, self.online, TAU)

        S_batch, A_batch, R_batch, S_Next_batch = self.memory.memory_sample(BATCH_SIZE)

        q_online = self.online.forward(S_batch).gather(1,A_batch)

        q_next = self.target.forward(S_Next_batch).max(1)[0].detach()

        q_target = R_batch + (GAMMA * q_next)

        self.loss = self.loss_func(q_online, q_target.unsqueeze(1))

        self.optimizer.zero_grad()
        self.loss.backward()
        self.optimizer.step()

    def save_nets(self, episode):

        torch.save(self.online.state_dict(), 'nets/_' + str(episode) + '_online.pt')

        print('nets saved successfully')

    def load_nets(self, episode):

        self.online.load_state_dict(torch.load('nets/_' + str(episode) + '_online.pt'))
        Tools.soft_update(self.target, self.online, TAU)
        print('nets loaded succesfully')
