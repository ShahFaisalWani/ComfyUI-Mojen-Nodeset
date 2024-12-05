import re
import spacy
from .utils import preprocess_common

nlp = spacy.load("en_core_web_sm")

STYLE_CATEGORIES = [
  'art_style', 
  'location', 
  'background', 
  'time_of_day',
  'setting'
]

def extract_multiple_values(input_string):
  extracted_values = {}
  for category in STYLE_CATEGORIES:
    pattern = rf"{category}: (.*?)(?=, \w+:|$)"
    match = re.search(pattern, input_string)
    if match:
      values = match.group(1).split(",")
      extracted_values[category] = [value.strip() for value in values if value.strip()]

  result_strings = []
  for key, values in extracted_values.items():
    result_strings.append(f"{key}: {', '.join(values)}")
  return ", ".join(result_strings)

def preprocess_style_text(text):
    text = extract_multiple_values(text)
    return preprocess_common(text)

def extract_style_tags(phrases):
    style_keywords = {"style", "art", "setting", "background", "scene"}
    style_tags = set()

    for phrase in phrases:
        doc = nlp(phrase.lower())
        if any(keyword in phrase.lower() for keyword in style_keywords):
            style_tags.add(phrase.strip())
        else:
            for token in doc:
                if token.text in style_keywords or token.pos_ in {"ADJ", "NOUN", "PROPN"}:
                    style_tags.add(phrase.strip())
                    break

    return style_tags

def process_style_text(text):
    phrases = preprocess_style_text(text)
    style_tags = extract_style_tags(phrases)
    return ', '.join(sorted(style_tags))

class StyleExtractorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_text": ("STRING", {}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_text",)
    FUNCTION = "process_style"
    CATEGORY = "Mojen/Custom"

    def process_style(self, input_text):
        style_tags = process_style_text(input_text)
        return (style_tags,)