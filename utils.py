import re

def preprocess_common(text):
  text = re.sub(r'[\'"]', '', text)
  no_keys = re.sub(r'\b[\w\s]+:\s*', '', text)
  no_semicolons = no_keys.replace(';', ',')
  no_na = re.sub(r'\bNA\b(?:[;\\]NA)*,?', '', no_semicolons)
  phrases = [phrase.strip() for phrase in no_na.split(',') if phrase.strip()]
  return list(dict.fromkeys(phrases))

def remove_1girl(phrases):
  items_to_remove = {"1girl", "1boy", "1man", "1woman"}
  items_to_remove = {item.lower() for item in items_to_remove}
  phrases = [phrase for phrase in phrases if phrase.lower() not in items_to_remove]
  return list(dict.fromkeys(phrases))