import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from model import *
class conv2D(nn.Module):
    def __init__(self, board_size, action_size, device, row, col):
        self.action_size=action_size
        self.device=device
        self.size = board_size
        self.row = row
        self.col = col
        # print(row, col)
        super(conv2D, self).__init__()
        # 1 input image channel, 6 output channels, 5x5 square convolution
        # kernel
        self.conv1 = nn.Conv2d(row, row, (2,2))
        self.conv2 = nn.Conv2d(row, row, (2,2))
        self.conv3 = nn.Conv2d(row, row, (2,2))
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(1575 , 100)  # 5*5 from image dimension
        # self.fc2 = nn.Linear(120, 84)
        # # Two heads on our network
        # self.action_head = nn.Linear(in_features=84, out_features=self.action_size)
        self.value_head = nn.Linear(in_features=100, out_features=1)

        self.to(device)

    def forward(self, x):
        # print("a",np.shape(x))
        # print(list(self.parameters()))
        # Max pooling over a (2, 2) window
        x=torch.FloatTensor(encodeboard2(np.array(x).reshape(self.row, self.col)))
        # print("b",np.shape(x))
        # print(list(self.parameters()))
        # print(np.shape(x))
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 4),1, 1)
        # print(np.shape(x))
        # If the size is a square, you can specify with a single number
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 4),1, 1)
        # print(np.shape(x))
        x = F.max_pool2d(F.relu(self.conv2(x)), (2, 4),1, 1)
        # x = F.max_pool2d(F.relu(self.conv3(x)), 2)
        # print(np.shape(x))
        y = torch.flatten(x, 1) # flatten all dimensions except the batch dimension
        y = F.relu(self.fc1(y))
        # x = F.relu(self.fc2(x))
        # x = self.fc3(x)
        # print(np.shape(x))
        # action_logits = self.action_head(x)
        value_logit = self.value_head(y)

        return F.softmax(x, dim=1), torch.sigmoid(value_logit)

    def predict(self, board):
        board = torch.FloatTensor(board.astype(np.float32)).to(self.device)
        board = board.view(1, self.size)
        self.eval()
        with torch.no_grad():
            pi, v = self.forward(board)
        # print("b",np.shape(pi))
        return pi.data.cpu().numpy()[0], v.data.cpu().numpy()[0]