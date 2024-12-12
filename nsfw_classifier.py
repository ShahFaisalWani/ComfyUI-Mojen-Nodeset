from transformers import pipeline
from PIL import Image, UnidentifiedImageError
from pathlib import Path
import torch
import numpy as np
import folder_paths
import os
from .utils import get_txt_file_counter
import re

class NSFWClassifierNode:
  def __init__(self):
    self.script_dir = Path(__file__).parent
    try:
      self.pipe = pipeline(
        "image-classification",
        model="giacomoarienti/nsfw-classifier",
        device=0 if torch.cuda.is_available() else -1
      )
    except Exception as e:
      print(f"Failed to initialize the NSFW classification pipeline: {e}")
      self.pipe = None

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "input_image": ("IMAGE", {}),
      }
    }

  OUTPUT_NODE = True
  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("nsfw_predictions",)
  FUNCTION = "process_nsfw"
  CATEGORY = "Mojen/Custom"

  def process_nsfw(self, input_image):
    try:
      if isinstance(input_image, torch.Tensor):
        image = self.tensor_to_pil(input_image)
        if image is None:
          return ("",)
      elif isinstance(input_image, np.ndarray):
        image = Image.fromarray(input_image)
      elif isinstance(input_image, str):
        try:
          image = Image.open(input_image).convert("RGB")
        except (FileNotFoundError, UnidentifiedImageError) as e:
          print(f"Failed to open image file: {e}")
          return ("",)
      elif isinstance(input_image, Image.Image):
        image = input_image
      else:
        print("Unsupported input type. Input must be a file path, a PIL.Image object, np.ndarray, or a torch.Tensor.")
        return ("",)

      if self.pipe:
        response = self.pipe(image)
        scores = {item['label']: round(item['score'] * 100, 2) for item in response}
        return (scores,)
      else:
        print("Pipeline is not initialized.")
        return ("",)
    except Exception as e:
      print(f"An error occurred during NSFW classification: {e}")
      return ("",)

  def tensor_to_pil(self, tensor):
    try:
      tensor = tensor.squeeze(0)
      if tensor.shape[0] == 3:
        tensor = tensor.permute(1, 2, 0)
      array = tensor.mul(255).byte().cpu().numpy()
      return Image.fromarray(array)
    except Exception as e:
      print(f"Failed to convert tensor to PIL.Image: {e}")
      return ("",)

class NSFWClassifierSaveNode(NSFWClassifierNode):
  def __init__(self):
    super().__init__()
    self.output_dir = folder_paths.get_output_directory()
    self.prefix_append = ""

  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "input_image": ("IMAGE", {}),
        "filename_prefix": ("STRING", {"default": "NSFWClassifier", "tooltip": "The prefix for the file to save."})
      }
    }

  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("nsfw_predictions",)
  FUNCTION = "process_and_store"
  CATEGORY = "Mojen/Custom"

  def generate_filename(self, path, prefix, delimiter, number_padding, extension):
    if number_padding == 0:
      filename = f"{prefix}{delimiter}{extension}"
    else:
      pattern = f"{re.escape(prefix)}{re.escape(delimiter)}(\d{{{number_padding}}}){re.escape(extension)}"

      existing_counters = [
        int(re.search(pattern, filename).group(1))
        for filename in os.listdir(path)
        if re.match(pattern, filename) and filename.endswith(extension)
      ]
      existing_counters.sort()
      if existing_counters:
        counter = existing_counters[-1] + 1
      else:
        counter = 1

      filename = f"{prefix}{delimiter}{counter:0{number_padding}}{extension}"

      while os.path.exists(os.path.join(path, filename)):
        counter += 1
        filename = f"{prefix}{delimiter}{counter:0{number_padding}}{extension}"

    return filename

  def process_and_store(self, input_image, filename_prefix):
    predictions = super().process_nsfw(input_image)
    if predictions and isinstance(predictions, tuple):
      predictions = predictions[0]
    if predictions == ("",):
      return ("",)

    output_file = self.generate_filename(
                    path=self.output_dir,
                    prefix=filename_prefix,
                    delimiter="_",
                    number_padding=5,
                    extension=".txt"
                  )

    try:
      with open(os.path.join(self.output_dir, output_file), "w") as file:
        file.write(f"{predictions}")

      print(f"Predictions stored in {output_file}")
      return (predictions,)

    except Exception as e:
      print(f"Failed to store predictions: {e}")
      return ("",)