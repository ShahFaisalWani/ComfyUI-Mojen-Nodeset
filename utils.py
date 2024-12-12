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

def get_txt_file_counter(output_dir, prefix):
    existing_files = list(output_dir.glob("*.txt"))
    prefix_counters = [
        int(file.stem.split('_')[-1])
        for file in existing_files
        if file.stem.startswith(prefix) and file.stem.split('_')[-1].isdigit()
    ]
    return max(prefix_counters, default=0) + 1
    self.prefix_append = ""