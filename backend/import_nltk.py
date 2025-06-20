# File: /my-fullstack-app/my-fullstack-app/backend/import_nltk.py

import nltk

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
    nltk.download("punkt_tab")
