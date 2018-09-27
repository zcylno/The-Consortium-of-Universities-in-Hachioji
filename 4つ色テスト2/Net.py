import torch.nn as nn
import torch.nn.functional as F


class Net(nn.Module):
    def __init__(self, action_dim):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=5, stride=2, padding=2)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5, stride=2, padding=2)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 32, kernel_size=5, stride=1, padding=2)
        self.bn3 = nn.BatchNorm2d(32)
        self.fc_1 = nn.Linear(25 * 25 * 32, 512)
        self.fc_2 = nn.Linear(512, action_dim)

    def forward(self, state):
        s_1 = F.relu(self.bn1(self.conv1(state)))
        s_2 = F.relu(self.bn2(self.conv2(s_1)))
        s_3 = F.relu(self.bn3(self.conv3(s_2)))
        s_4 = F.relu(self.fc_1(s_3.view(s_3.size(0), -1)))
        action = self.fc_2(s_4.view(s_4.size(0), -1))

        return action