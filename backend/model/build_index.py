import os
import pickle
from collections import Counter
from nltk.util import ngrams

from model.normalize import normalize
from model.read_corpus import read_corpus

def build_index():
    INDEX_DIR = r'src/index'
    os.makedirs(INDEX_DIR, exist_ok=True)
    berita_list, file_names = read_corpus()
    counts_per_doc = {}

    total_unigram = Counter()
    total_bigram = Counter()
    total_trigram = Counter()
    vocabulary_size = 0
    vocabulary = set()

    for idx, teks in enumerate(berita_list):
        fname = file_names[idx]
        stem_tokens = normalize(teks)
        unigram = Counter(stem_tokens)
        bigram = Counter(list(ngrams(stem_tokens, 2)))
        trigram = Counter(list(ngrams(stem_tokens, 3)))
        counts_per_doc[fname] = {
            "unigram": unigram,
            "bigram": bigram,
            "trigram": trigram
        }
        vocabulary.update(stem_tokens)
        total_unigram.update(unigram)
        total_bigram.update(bigram)
        total_trigram.update(trigram)

    vocabulary_size = len(vocabulary)

    with open(os.path.join(INDEX_DIR, "counts_per_doc.pkl"), "wb") as f:
        pickle.dump(counts_per_doc, f)
    with open(os.path.join(INDEX_DIR, "total_unigram.pkl"), "wb") as f:
        pickle.dump(total_unigram, f)
    with open(os.path.join(INDEX_DIR, "total_bigram.pkl"), "wb") as f:
        pickle.dump(total_bigram, f)
    with open(os.path.join(INDEX_DIR, "total_trigram.pkl"), "wb") as f:
        pickle.dump(total_trigram, f)
    with open(os.path.join(INDEX_DIR, "total_vocabulary.pkl"), "wb") as f:
        pickle.dump(vocabulary_size, f)

    return (counts_per_doc, total_unigram, total_bigram, total_trigram, vocabulary_size)