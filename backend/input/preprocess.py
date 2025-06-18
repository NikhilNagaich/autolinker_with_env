# File: /my-fullstack-app/my-fullstack-app/backend/input/preprocess.py

import nltk
from typing import List

def clean_text(text: str) -> List[str]:
    sentences = nltk.sent_tokenize(text)

    clean_sentences = []
    for s in sentences:
        s = s.strip().replace("\n", " ")
        if 20 < len(s) < 500:
            clean_sentences.append(s)

    return clean_sentences