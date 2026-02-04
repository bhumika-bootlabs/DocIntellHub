import re
from collections import Counter

def effective_extractive_summary(text: str, max_sentences: int = 4) -> str:
    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Split into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    if len(sentences) <= max_sentences:
        return text

    # Tokenize words
    words = re.findall(r'\w+', text.lower())
    freq = Counter(words)

    # Score sentences
    sentence_scores = {}
    for sent in sentences:
        sent_words = re.findall(r'\w+', sent.lower())
        score = sum(freq[w] for w in sent_words)
        sentence_scores[sent] = score

    # Pick top N sentences
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]

    return " ".join(top_sentences)

