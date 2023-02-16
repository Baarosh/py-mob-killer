from base_processor import BaseProcessor
import numpy as np

class RGBtoGrayScaleProcessor(BaseProcessor):
    ...

    def process_frame(frame: np.ndarray) -> np.ndarray:
        return super().process_frame()




d = {'rgb_to_grayscale': RGBtoGrayScaleProcessor,
     }




z = d.get('rgb_to_grayscale')().process_frame
print(z)