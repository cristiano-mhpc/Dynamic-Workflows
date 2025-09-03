import copy 
from typing import Dict, List

import torch 
import torch.nn as nn 

from .base_server import BaseServer

class FedAvgServer(BaseServer):
    """Federated Averaging server class"""

    def __init__(self, model: nn.Module, device: torch.device = torch.device("cpu")):
        """Constructor
        :param model: DNN model
        :type model: nn.Module
        """
        self.model = copy.deepcopy(model).to(device)
        self.device = device

    def get_model(self) -> nn.Module:
        """Returns a (deep) copy of the DNN model

        :return: copy of the DNN model
        :rtype: nn.Module
        """
        return copy.deepcopy(self.model).to(self.device)

    def get_parameters(self) -> Dict[str, torch.Tensor]:
        """Returns a (deep) copy of the DNN model

        :return: copy of the DNN model
        :rtype: Dict[str, torch.Tensor]
        """
        return copy.deepcopy(self.model.state_dict())

    def average(self, state_dicts: List[Dict[str, torch.Tensor]]) -> None:
        """Aerage the parameters from a list of client models."""
        if not state_dicts:
            raise ValueError("No state_dicts to average.")

        # Initialize the accumulator with the first model's state_dict (deep copy)
        avg_state_dict = copy.deepcopy(state_dicts[0])

        # Accumulate parameters from the reamining models  
        for state_dict in state_dicts[1:]:
            for key in state_dict:
                avg_state_dict[key] += state_dict[key]

        # Divide by the number of the models to get the average 
        num_models = len(state_dicts)
        for key in avg_state_dict:
            avg_state_dict[key] /= num_models
        
        # Update the server's model with the averaged parameters
        self.model.load_state_dict(avg_state_dict)
