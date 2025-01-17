# import logging
# from comfy.utils import ProgressBar
# import time

# class AnyType(str):
#   """A special class that is always equal in not equal comparisons. Credit to pythongosssss"""

#   def __ne__(self, __value: object) -> bool:
#     return False

# any_type = AnyType("*")

# class LogPercentNode:
#   @classmethod
#   def INPUT_TYPES(cls):
#     return {
#       "optional": {
#         "anything": (any_type, {}),
#         "percent": ("INT", {}),
#       },
#       "hidden": {
#         "unique_id": "UNIQUE_ID",
#         "extra_pnginfo": "EXTRA_PNGINFO",
#       }
#     }

#   RETURN_TYPES = (any_type,)
#   RETURN_NAMES = ('output',)
#   FUNCTION = "log_and_pass"
#   CATEGORY = "Mojen/Custom"

#   def log_and_pass(self, anything, percent, unique_id=None, extra_pnginfo=None):
#     pbar = ProgressBar(percent)
#     time.sleep(0.1)
#     pbar.update_absolute(percent, percent, preview=None, node="mojen_percent")

#     logging.info(f"PROGRESS: {percent}%")
#     return (anything,)

class StringLengthNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_string": ("STRING", {}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
                "extra_pnginfo": "EXTRA_PNGINFO",
            }
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("string_length",)
    FUNCTION = "compute_length"
    CATEGORY = "Mojen/Custom"

    def compute_length(self, input_string, unique_id=None, extra_pnginfo=None):
        string_length = len(input_string)
        return (string_length,)