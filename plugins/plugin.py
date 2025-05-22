from abc import ABC, abstractmethod

class Plugin(ABC):
    @abstractmethod

    def get_weights(self, rebalance)-> dict[float]:
        pass
