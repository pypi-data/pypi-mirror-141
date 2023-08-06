from typing import Dict, List

import torch

from ..core.abstractparameter import AbstractParameter
from ..core.utils import process_objects, register_class
from .convergence import BaseConvergence


@register_class
class PlugConvergence(BaseConvergence):
    """Class that does not check for convergence but output ELBO.

    :param List[AbstractParameter] paramters: list of parameters
    :param int every: evaluate ELBO at every "every" iteration
    """

    def __init__(
        self,
        parameters: List[AbstractParameter],
        every: int,
    ) -> None:
        self.parameters = parameters
        self.every = every
        self.previous_grad = [None] * len(self.parameters)
        self.S = [0.0] * len(self.parameters)

    def check(self, iteration: int, *args, **kwargs) -> bool:
        if iteration == 1:
            for idx, p in enumerate(self.parameters):
                self.previous_grad[idx] = p.tensor.grad.clone()
        elif iteration % self.every == 0:
            for idx, p in enumerate(self.parameters):
                self.S[idx] += torch.sum(
                    self.previous_grad[idx] * p.tensor.grad.clone()
                )
                self.previous_grad[idx] = p.tensor.grad.clone()
                print(f"{p.id} {self.S[idx]} {p.tensor.grad.clone().mean()}")
        return True

    @classmethod
    def from_json(cls, data: Dict[str, any], dic: Dict[str, any]) -> 'PlugConvergence':
        parameters = process_objects(data['parameters'], dic)
        every = data.get('every', 100)
        return cls(parameters, every)
