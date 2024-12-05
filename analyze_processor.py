import re
import json
from .utils import preprocess_common, remove_1girl

def process_analyze(input_text):
  if "\n\n" in input_text:
    first_part, second_part = input_text.split("\n\n", 1)
  else:
    first_part = input_text
    second_part = ""

  if "camera_angle" in second_part:
    second_part_tags = preprocess_common(second_part)
  else:
    second_part_tags = [tag.strip() for tag in re.split(r"[,.]", second_part) if tag.strip()]

  first_part_tags = [tag.strip() for tag in re.split(r"[,.]", first_part) if tag.strip()]

  primary_tags = first_part_tags[:3]
  remaining_tags = first_part_tags[3:]

  merged_tags = list(dict.fromkeys(remaining_tags + second_part_tags))

  primary_tags = remove_1girl(list(dict.fromkeys(primary_tags)))
  secondary_tags = remove_1girl(merged_tags)

  primary_tags_str = ",".join(primary_tags)
  secondary_tags_str = ",".join(secondary_tags)
  output_dict = {
    'primary': primary_tags_str,
    'secondary': secondary_tags_str,
  }

  analyze_output = json.dumps(output_dict)

  return primary_tags_str, secondary_tags_str, analyze_output

class AnalyzeProcessorNode:
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "input_text": ("STRING", {}),
      }
    }

  RETURN_TYPES = ("STRING", "STRING", "STRING")
  RETURN_NAMES = ("primary_tags", "secondary_tags", "analyze_output")
  FUNCTION = "process_split_text"
  CATEGORY = "Mojen/Custom"

  def process_split_text(self, input_text):
    return process_analyze(input_text)
