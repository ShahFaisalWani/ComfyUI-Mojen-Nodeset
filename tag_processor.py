import re
import spacy
from .utils import preprocess_common, remove_1girl

nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
  return preprocess_common(text)

def preprocess_down_text(text):
  processed_text = preprocess_common(text)
  return remove_1girl(processed_text)

def extract_noun_chunks(phrases):
  processed_phrases = set()
  for phrase in phrases:
    doc = nlp(phrase.lower())
    if any(token.pos_ == "PROPN" for token in doc) or all(token.is_alpha or token.is_digit for token in doc):
      processed_phrases.add(phrase.strip())
      continue
    for chunk in doc.noun_chunks:
      chunk_tokens = [token.text for token in chunk if token.pos_ not in {"DET"}]
      processed_phrases.add(" ".join(chunk_tokens).strip())
    if not list(doc.noun_chunks):
      for token in doc:
        if token.pos_ in {"NOUN", "PROPN", "ADJ"} and not token.is_stop and token.pos_ != "DET":
          processed_phrases.add(token.text.strip())
  return processed_phrases

def split_long_phrases(combined_tags):
  final_tags = set()
  for tag in combined_tags:
    doc = nlp(tag.lower())
    meaningful_tokens = [
      token.text for token in doc if token.pos_ in {"NOUN", "PROPN", "ADJ", "VERB"} and not token.is_stop
    ]
    simplified_phrase = " ".join(meaningful_tokens)
    if len(meaningful_tokens) > 0 and len(simplified_phrase.split()) <= 3:
      final_tags.add(simplified_phrase.strip())
  return final_tags

def process_texts(top_text, down_text):
  top_phrases = preprocess_text(top_text)
  simplified_top = extract_noun_chunks(top_phrases)
  simplified_top = split_long_phrases(simplified_top)
  down_phrases = preprocess_down_text(down_text)
  simplified_down = extract_noun_chunks(down_phrases)
  final_tags = simplified_top.union(simplified_down)
  return ', '.join(sorted(final_tags))

class TagProcessorNode:
  @classmethod
  def INPUT_TYPES(cls):
    return {
      "required": {
        "top_text": ("STRING", {}),
        "down_text": ("STRING", {}),
      }
    }

  RETURN_TYPES = ("STRING",)
  RETURN_NAMES = ("processed_text",)
  FUNCTION = "process"
  CATEGORY = "Mojen/Custom"

  def process(self, top_text, down_text):
    processed_text = process_texts(top_text, down_text)
    return (processed_text,)
