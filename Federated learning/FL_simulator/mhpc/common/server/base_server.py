"""Abstract base class for FL servers"""

from abc import ABC, abstractmethod
from typing import Dict, List

import torch
import torch.nn as nn


class BaseServer(ABC):

    @abstractmethod
    def get_model(self) -> nn.Module:
        """Returns a (deep) copy of the DNN model

        :return: copy of the DNN model
        :rtype: nn.Module
        """
        pass

    @abstractmethod
    def get_parameters(self) -> Dict[str, torch.Tensor]:
        """Returns a (deep) copy of the DNN model

        :return: copy of the DNN model
        :rtype: Dict[str, torch.Tensor]
        """

    @abstractmethod
    def average(self, models: List[nn.Module]) -> None:
        """Sets the server's model to the average of the clients' models

        :param models: List of clients' models
        :type models: List[nn.Module]
        """
        pass
