import re
from collections import Counter

STOPWORDS = {
    "the","is","and","to","of","in","that","we","a","for","it","on","with",
    "as","this","was","are","be","by","an","or","from","at","but","not"
}

def effective_extractive_summary(text: str, max_sentences: int = 4) -> str:
    
    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Split sentences
    sentences = re.split(r'(?<=[.!?]) +', text)

    if len(sentences) <= max_sentences:
        return text

    # Tokenize and remove stopwords
    words = re.findall(r'\w+', text.lower())
    words = [w for w in words if w not in STOPWORDS]

    freq = Counter(words)

    # Score sentences
    sentence_scores = {}

    for sent in sentences:
        sent_words = re.findall(r'\w+', sent.lower())
        sent_words = [w for w in sent_words if w not in STOPWORDS]

        if not sent_words:
            continue

        score = sum(freq[w] for w in sent_words) / len(sent_words)  # normalize
        sentence_scores[sent] = score

    # Select top sentences
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:max_sentences]

    # Preserve original order
    ordered_summary = [s for s in sentences if s in top_sentences]

    return " ".join(ordered_summary)

