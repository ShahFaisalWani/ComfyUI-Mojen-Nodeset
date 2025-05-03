import numpy as np
from PIL import Image
import torch

class TransparentBgNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "target_color": (["white", "black"],),
                "tolerance": ("INT", {
                    "default": 10,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "slider"
                }),
                "opacity": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 255,
                    "step": 1,
                    "display": "slider"
                }),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "convert_to_transparent"
    CATEGORY = "image/processing"

    def convert_to_transparent(self, image, target_color, tolerance, opacity):
        batch_size, height, width, channels = image.shape
    
        result_batch = []
        
        for b in range(batch_size):
            img_np = image[b].cpu().numpy() * 255
            img_np = img_np.astype(np.uint8)
            
            rgb = img_np[:, :, :3]
            
            if channels > 3:
                alpha = img_np[:, :, 3].copy()
            else:
                alpha = np.full((height, width), 255, dtype=np.uint8)
            
            if target_color.lower() == 'white':
                mask = np.all(rgb >= 255 - tolerance, axis=2)
            elif target_color.lower() == 'black':
                mask = np.all(rgb <= 0 + tolerance, axis=2)
            else:
                raise ValueError("Target color must be either 'white' or 'black'")
            
            alpha[mask] = opacity
            
            result_array = np.dstack((rgb, alpha))
            
            result_tensor = torch.from_numpy(result_array.astype(np.float32) / 255.0)
            result_batch.append(result_tensor)
        
        return (torch.stack(result_batch),)
