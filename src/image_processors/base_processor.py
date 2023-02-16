from abc import ABC, abstractmethod
import numpy as np



class BaseProcessor(ABC):
    def __init__(self) -> None:
        super().__init__()

    def printer(self):
        print('dupstzal')
    @abstractmethod
    def process_frame(frame: np.ndarray) -> np.ndarray:
        print('dupsko')



x = BaseProcessor()