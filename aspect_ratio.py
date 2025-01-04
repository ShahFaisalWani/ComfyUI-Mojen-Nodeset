import hashlib

class AspectRatioNode:
  @classmethod
  def INPUT_TYPES(cls):
    aspect_ratios = [
      "1:1",
      "4:5",
      "2:3",
      "3:5",
      "9:16",
      "5:4",
      "3:2",
      "5:3",
      "16:9",
    ]        
    return {"required": {"aspect_ratio": (aspect_ratios,)}}

  FUNCTION = "calculate_dimensions"
  RETURN_TYPES = ("INT", "INT")
  RETURN_NAMES = ("WIDTH", "HEIGHT")
  CATEGORY = "Mojen/Custom"

  def calculate_dimensions(self, aspect_ratio):
    BASE_DIM = 1024
    BASE_FACTOR = 16
    w_ratio, h_ratio = map(int, aspect_ratio.split(':'))
    ratio = w_ratio / h_ratio

    base_area = BASE_DIM ** 2
    target_area = base_area

    width = int((target_area * ratio) ** 0.5)
    height = int(target_area / width)

    width = (width // BASE_FACTOR) * BASE_FACTOR
    height = (height // BASE_FACTOR) * BASE_FACTOR

    while round(width / height, 5) != round(ratio, 5):
      if width / height < ratio:
        width += BASE_FACTOR
      else:
        width -= BASE_FACTOR
      height = int(width / ratio)
      height = (height // BASE_FACTOR) * BASE_FACTOR

    return width, height

  @classmethod
  def IS_CHANGED(cls, aspect_ratio):
    return hashlib.sha256(aspect_ratio.encode('utf-8')).hexdigest()

  @classmethod
  def VALIDATE_INPUTS(cls, aspect_ratio):
    try:
      w, h = map(int, aspect_ratio.split(':'))
      return w > 0 and h > 0
    except:
      return False
