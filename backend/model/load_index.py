import os
import pickle
from model.build_index import build_index

def load_index():
    INDEX_DIR = r'src/index/'
    pickle_files = [
        "counts_per_doc.pkl",
        "total_unigram.pkl",
        "total_bigram.pkl",
        "total_trigram.pkl",
        "total_vocabulary.pkl"
    ]
    missing = [f for f in pickle_files if not os.path.isfile(os.path.join(INDEX_DIR, f))]

    if missing:
        build_index()
        # raise FileNotFoundError(
        #     f"File index hilang: {missing}. Silakan bangun index terlebih dahulu (build_index())."
        # )

    with open(os.path.join(INDEX_DIR, "counts_per_doc.pkl"), "rb") as f:
        counts_per_doc = pickle.load(f)
    with open(os.path.join(INDEX_DIR, "total_unigram.pkl"), "rb") as f:
        total_unigram = pickle.load(f)
    with open(os.path.join(INDEX_DIR, "total_bigram.pkl"), "rb") as f:
        total_bigram = pickle.load(f)
    with open(os.path.join(INDEX_DIR, "total_trigram.pkl"), "rb") as f:
        total_trigram = pickle.load(f)
    with open(os.path.join(INDEX_DIR, "total_vocabulary.pkl"), "rb") as f:
        total_vocabulary = pickle.load(f)

    return counts_per_doc, total_unigram, total_bigram, total_trigram, total_vocabulary