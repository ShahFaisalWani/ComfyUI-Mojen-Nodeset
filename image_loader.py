import os
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence, UnidentifiedImageError
from io import BytesIO
import hashlib
import folder_paths
import node_helpers
import pillow_avif

class ImageLoader:
  @classmethod
  def INPUT_TYPES(s):
    input_dir = folder_paths.get_input_directory()
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    return {"required": {"image": (sorted(files), {"image_upload": True})}}

  CATEGORY = "image"
  RETURN_TYPES = ("IMAGE", "MASK")
  FUNCTION = "load_image"

  def load_image(self, image):
    image_path = folder_paths.get_annotated_filepath(image)
    try:
      with open(image_path, "rb") as f:
        img_data = f.read()
        img = Image.open(BytesIO(img_data))
    except (UnidentifiedImageError, SyntaxError):
      with open(image_path, "rb") as f:
        repaired_data = self.repair_image(f.read())
        img = Image.open(BytesIO(repaired_data))
    img = self.ensure_srgb(img)
    img = node_helpers.pillow(ImageOps.exif_transpose, img)
    img = img.convert("RGB")
    output_images = []
    output_masks = []
    w, h = img.size
    for i in ImageSequence.Iterator(img):
      image = np.array(i).astype(np.float32) / 255.0
      image = torch.from_numpy(image)[None,]
      mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
      output_images.append(image)
      output_masks.append(mask.unsqueeze(0))
    output_image = torch.cat(output_images, dim=0) if len(output_images) > 1 else output_images[0]
    output_mask = torch.cat(output_masks, dim=0) if len(output_masks) > 1 else output_masks[0]
    return output_image, output_mask

  def repair_image(self, data):
    if data[:2] != b"\xff\xd8":
      return b"\xff\xd8" + data[2:]
    return data

  def ensure_srgb(self, img):
    try:
      if img.info.get("icc_profile"):
        img = ImageOps.autocontrast(img)
        img = img.convert("RGB", colors=256)
    except Exception:
      pass
    return img

  @classmethod
  def IS_CHANGED(s, image):
    image_path = folder_paths.get_annotated_filepath(image)
    m = hashlib.sha256()
    with open(image_path, 'rb') as f:
      m.update(f.read())
    return m.digest().hex()

  @classmethod
  def VALIDATE_INPUTS(s, image):
    if not folder_paths.exists_annotated_filepath(image):
      return "Invalid image file: {}".format(image)
    return True
