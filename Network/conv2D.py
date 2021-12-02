import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
class conv2D(nn.Module):
    def __init__(self, board_size, action_size, device):

        super(conv2D, self).__init__()

        self.device = device
        self.size = board_size
        self.action_size = action_size
        
        self.fc1 = nn.Linear(in_features=self.size, out_features=board_size*2)
        self.fc2 = nn.Linear(in_features=board_size*2, out_features=board_size*4)

        # Two heads on our network
        self.action_head = nn.Linear(in_features=board_size*4, out_features=self.action_size)
        self.value_head = nn.Linear(in_features=board_size*4, out_features=1)

        self.to(device)

    def forward(self, x):
        print("a",np.shape(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        
        action_logits = self.action_head(x)
        value_logit = self.value_head(x)

        return F.softmax(action_logits, dim=1), torch.sigmoid(value_logit)

    def predict(self, board):
        board = torch.FloatTensor(board.astype(np.float32)).to(self.device)
        board = board.view(1, self.size)
        self.eval()
        with torch.no_grad():
            pi, v = self.forward(board)
        print("b",np.shape(pi))
        return pi.data.cpu().numpy()[0], v.data.cpu().numpy()[0]