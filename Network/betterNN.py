import numpy as np
from tensorflow.python.framework.ops import inside_function

import torch
import torch.nn as nn
import torch.nn.functional as F


class betterNN(nn.Module):

    def __init__(self, board_size, action_size, device):

        super(betterNN, self).__init__()

        self.device = device
        self.size = board_size
        self.action_size = action_size
        
        self.conv_1 = nn.Conv2d(in_channels=self.size, out_channels=board_size*2, kernel_size=1)
        self.bn_1 = nn.BatchNorm2d(board_size*2)
        self.conv_2 = nn.Conv2d(in_channels=board_size*2, out_channels=board_size*4, kernel_size=1, stride=1, padding='same')
        self.bn_2  = nn.BatchNorm2d(board_size*4)
        self.conv_3 = nn.Conv2d(in_channels=board_size*4, out_channels=board_size*6, kernel_size=1, padding='same')
        self.bn_3 = nn.BatchNorm2d(board_size*6)

        # Two heads on our network
        self.action_head = nn.Linear(in_features=board_size*6, out_features=self.action_size)
        self.value_head = nn.Linear(in_features=board_size*6, out_features=1)

        self.to(device)

    def forward(self, x):
        x = F.relu(self.bn_1(self.conv_1(x)))
        x = F.relu(self.bn_2(self.conv_2(x)))
        x = F.relu(self.bn_3(self.conv_3(x)))

        action_logits = self.action_head(x)
        value_logit = self.value_head(x)

        return F.softmax(action_logits, dim=1), F.tanh(value_logit)

    def predict(self, board):
        board = torch.FloatTensor(board.astype(np.float32)).to(self.device)
        board = board.view(1, self.size)
        self.eval()
        with torch.no_grad():
            pi, v = self.forward(board)

        return pi.data.cpu().numpy()[0], v.data.cpu().numpy()[0]