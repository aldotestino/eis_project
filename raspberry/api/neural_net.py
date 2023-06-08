import torch
import torch.nn as nn
import torch.nn.functional as func

class NeuralNet(nn.Module):
  def __init__(self, n_features):
    super(NeuralNet, self).__init__()
    self.fc1 = nn.Linear(n_features, 64)
    self.fc2 = nn.Linear(64, 128)
    self.fc3 = nn.Linear(128, 1)

    self.dropout = nn.Dropout(0.2)

  def forward(self, x):
    x = func.relu(self.fc1(x))
    x = func.relu(self.fc2(x))
    return torch.sigmoid(self.fc3(x))
  
