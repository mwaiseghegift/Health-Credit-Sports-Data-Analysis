import re
import sys

if len(sys.argv) != 2:
    print("Usage: python clean_emojis.py <filepath>")
    sys.exit(1)

filepath = sys.argv[1]

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: File '{filepath}' not found.")
    sys.exit(1)

# Regex to match emojis (covers most common ranges)
emoji_pattern = re.compile(
    r'[\U0001F600-\U0001F64F'  # emoticons
    r'\U0001F300-\U0001F5FF'  # symbols & pictographs
    r'\U0001F680-\U0001F6FF'  # transport & map symbols
    r'\U0001F1E0-\U0001F1FF'  # flags
    r'\U00002700-\U000027BF'  # dingbats
    r'\U0001f926-\U0001f937'  # gestures
    r'\U00010000-\U0010ffff'  # other misc
    r'\u2640-\u2642'  # gender symbols
    r'\u2600-\u2B55'  # misc symbols
    r'\u2300-\u23FF'  # misc technical
    r'\u200d'  # zero width joiner
    r'\ufe0f'  # variation selector
    r'\u3030'  # wavy dash
    r']+', flags=re.UNICODE)

cleaned = emoji_pattern.sub('', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(cleaned)

print(f"Emojis removed from '{filepath}'.")
