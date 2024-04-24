import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

num_features = 13
num_classes = 8

class GenreDataset(Dataset):
    def __init__(self, data, label) -> None:
        super(GenreDataset, self).__init__()
        self.data = torch.tensor(data).to(torch.float32)
        self.label = torch.tensor(label).to(torch.long)
    def __len__(self):
        return self.data.size(0)
    def __getitem__(self, index):
        return self.data[index], self.label[index]
    
class NN(nn.Module):
    def __init__(self, num_features, num_classes) -> None:
        super(NN, self).__init__()
        self.model = nn.Sequential(nn.BatchNorm1d(num_features),
                                   nn.Linear(num_features, 64),
                                   nn.BatchNorm1d(64),
                                   nn.ReLU(),
                                   nn.Dropout(0.2),
                                   nn.Linear(64, 128),
                                   nn.BatchNorm1d(128),
                                   nn.ReLU(),
                                   nn.Dropout(0.3),
                                   nn.Linear(128, 128),
                                   nn.BatchNorm1d(128),
                                   nn.ReLU(),
                                   nn.Dropout(0.4),
                                   nn.Linear(128, num_classes))
    def forward(self, x):
        logits = self.model(x)
        return logits
    
def eval(model: nn.Module, dataset: GenreDataset) -> float:
    dataloader = DataLoader(dataset, batch_size=1024)
    model.eval()
    correct = 0
    total = 0
    for data, label in dataloader:
        logits = model(data)
        pred = torch.argmax(logits, 1)
        correct += torch.sum(pred == label)
        total += len(data)
    return correct / total

def train(num_epochs: int=50,
          lr: float=0.001,
          batch_size: int=128):
    
    train_data = np.load('train_data.npy')
    train_label = np.load('train_label.npy')
    train_dataset = GenreDataset(train_data, train_label)
    model = NN(num_features, num_classes)
    
    model.train()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr)
    train_dataloader = DataLoader(train_dataset, batch_size)

    num_iters = 0

    for i in range(num_epochs):
        for _, (train_data, train_label) in enumerate(train_dataloader):
            logits = model(train_data)
            loss = criterion(logits, train_label)
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            num_iters += 1

        print(f'Epoch {i}: Training acc: {eval(model, train_dataset)}')
        model.train()

    torch.save(model.state_dict(), 'nn.pth')

def test():
    test_data = np.load('test_data.npy')
    test_label = np.load('test_label.npy')
    test_dataset = GenreDataset(test_data, test_label)
    model = NN(num_features, num_classes)
    model.load_state_dict(torch.load('nn.pth'))
    print(f'Testing acc: {eval(model, test_dataset)}')


def main() -> None:
    # train()
    test()
    
    pass
    

if __name__ == '__main__':
    main()
