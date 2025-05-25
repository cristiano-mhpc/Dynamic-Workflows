import copy 
from typing import Dict, Tuple 
import torch 
import torch.nn as nn 
import torch.optim as optim
from torch.utils.data import DataLoader

from .base_client import BaseClient

class FedAvgClient(BaseClient):
    def __init__(
        self, client_id: int,
        model: nn.Module, 
        train_loader: DataLoader, 
        test_loader: DataLoader, 
        lr: float = 0.01, 
        device: torch.device = torch.device("cpu")):

        self.client_id = client_id 
        self.model = copy.deepcopy(model).to(device)
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.device = device
        self.optimizer = optim.SGD(self.model.parameters(),lr=lr)
        self.loss_fn = nn.CrossEntropyLoss()

    def set_model(self, model: nn.Module) -> None:
        """Sets the client's model

        :param model: DNN model assigned to the client
        :type model: nn.Module
        """
        self.model = copy.deepcopy(model).to(self.device)
        self.optimizer = optim.SGD(self.model.parameters(), lr=self.optimizer.param_groups[0]['lr'])

    def set_parameters(self, state_dict: Dict[str, torch.Tensor]) -> None:
        """Sets the client's model

        :param model: DNN model assigned to the client
        :type model: Dict[str, torch.Tensor]
        """
        self.model.load_state_dict(copy.deepcopy(state_dict))
    
    def get_parameters(self) -> Dict[str, torch.Tensor]:
        """Returns the client's model parameters

        :return: The client's DNN model
        :rtype: Dict[str, torch.Tensor]
        """
        return copy.deepcopy(self.model.state_dict())


    def train(self, epochs: int = 2) -> float:
        """Training of the client's model

        :param epochs: Number of training epochs to run, defaults to 1
        :type epochs: int, optional
        :return: Final training loss
        :rtype: float
        """
        self.model.train()
        total_loss = 0.0

        for _ in range(epochs):
            for inputs, targets in self.train_loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                self.optimizer.zero_grad()
                outputs = self.model(inputs)
                loss = self.loss_fn(outputs, targets)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
        return total_loss / (len(self.train_loader)*epochs)


    def test(self) -> Tuple[float, float]:
        """Testing of the client's local model

        :return: Final testing loss and accuracy
        :rtype: Tuple[float, float]
        """
        self.model.eval()
        correct = 0 
        total = 0
        total_loss = 0.0
        with torch.no_grad():
            for inputs, targets in self.test_loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)
                outputs = self.model(inputs)
                loss = self.loss_fn(outputs, targets)
                total_loss += loss.item()
                preds = outputs.argmax(dim=1)
                correct += (preds == targets).sum().item()
                total += targets.size(0)

        accuracy = correct / total
        avg_loss = total_loss / len(self.test_loader)
        return avg_loss, accuracy






