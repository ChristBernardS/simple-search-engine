from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from model.ngram_LM import ngram_LM
from model.build_index import build_index
from model.load_index import load_index

from model.tf_idf import tf_idf
from model.snippet import generate_snippet
from model.read_corpus import read_corpus

app = Flask(__name__)
frontend_url = "https://simple-search-engine-ui.netlify.app"
cors = CORS(app, resources={r"/predict*": {"origins": frontend_url}})

# Load model saat startup
try:
    counts_per_doc, total_unigram, total_bigram, total_trigram, total_vocabulary = load_index()
    corpus_docs, file_names = read_corpus()
    doc_map = {fn: text for fn, text in zip(file_names, corpus_docs)}
except FileNotFoundError:
    print(">> File index tidak ditemukan. Membuat index baru …")
    counts_per_doc, total_unigram, total_bigram, total_trigram, total_vocabulary = build_index()
    corpus_docs, file_names = read_corpus()
    doc_map = {fn: text for fn, text in zip(file_names, corpus_docs)}

@app.route("/")
def home():
    return jsonify({"message": "Flask server is running!"})

@app.route("/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    query = data.get("query", "")

    # 1. Dapatkan prediksi N-gram (logika yang sudah ada)
    ngram_results = ngram_LM(query, total_unigram, total_bigram, total_trigram, total_vocabulary)
    predictions = {kata: prob for kata, prob in ngram_results}

    # 2. Hitung relevansi dokumen dengan TF-IDF
    relevance_scores = tf_idf([query.lower()])
    
    # 3. Buat daftar dokumen relevan dengan snippet
    relevant_docs = []
    keywords = query.lower().split()
    
    # Ambil top 10 dokumen relevan
    for doc_name, score in relevance_scores.head(10).items():
        if score > 0:
            document_text = doc_map.get(doc_name, "")
            snippet = generate_snippet(document_text, query)
            relevant_docs.append({
                "document": doc_name,
                "score": round(score, 5),
                "snippet": snippet
            })

    # 4. Gabungkan semua hasil ke dalam satu JSON response
    final_result = {
        "predictions": predictions,
        "documents": relevant_docs
    }

    return jsonify(final_result)

@app.route("/build", methods=["POST"])
def api_build():
    build_index()
    return jsonify({"status": "ok", "message": "Index berhasil dibuat / diperbarui"})

if __name__ == "__main__":
    app.run()