"""Abstract base class for FL clients"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple

import torch
import torch.nn as nn


class BaseClient(ABC):

    @abstractmethod
    def set_model(self, model: nn.Module) -> None:
        """Sets the client's model

        :param model: DNN model assigned to the client
        :type model: nn.Module
        """
        pass

    @abstractmethod
    def set_parameters(self, state_dict: Dict[str, torch.Tensor]) -> None:
        """Sets the client's model

        :param model: DNN model assigned to the client
        :type model: Dict[str, torch.Tensor]
        """
        pass

    @abstractmethod
    def get_parameters(self) -> Dict[str, torch.Tensor]:
        """Returns the client's model parameters

        :return: The client's DNN model
        :rtype: tuple[str, torch.Tensor]
        """
        pass

    @abstractmethod
    def train(self, epochs: int = 1) -> float:
        """Training of the client's model

        :param epochs: Number of training epochs to run, defaults to 1
        :type epochs: int, optional
        :return: Final training loss
        :rtype: float
        """
        pass

    @abstractmethod
    def test(self) -> Tuple[float, float]:
        """Testing of the client's local model

        :return: Final testing loss and accuracy
        :rtype: Tuple[float, float]
        """
        pass
