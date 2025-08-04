import os
import sys
import serverless_wsgi
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Perubahan Penting untuk Path ---
# Menambahkan root direktori proyek ke path agar impor model berfungsi
# Ini membuat 'import model.ngram_LM' bisa ditemukan oleh Netlify
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
# ------------------------------------

from model.ngram_LM import ngram_LM
from model.build_index import build_index
from model.load_index import load_index
from model.tf_idf import tf_idf
from model.snippet import generate_snippet
from model.read_corpus import read_corpus

# Inisialisasi aplikasi Flask tetap sama
app = Flask(__name__)
CORS(app) # Mengizinkan semua origin, aman untuk Netlify Functions

# Logika untuk load model dan data tetap sama.
# Path akan otomatis benar karena kita sudah mengatur sys.path di atas.
try:
    counts_per_doc, total_unigram, total_bigram, total_trigram, total_vocabulary = load_index()
    corpus_docs, file_names = read_corpus()
    doc_map = {fn: text for fn, text in zip(file_names, corpus_docs)}
except FileNotFoundError:
    print(">> File index tidak ditemukan. Membuat index baru …")
    counts_per_doc, total_unigram, total_bigram, total_trigram, total_vocabulary = build_index()
    corpus_docs, file_names = read_corpus()
    doc_map = {fn: text for fn, text in zip(file_names, corpus_docs)}

# --- Perubahan Penting pada Rute ---
# Tambahkan prefix /api/ pada semua rute agar sesuai dengan konfigurasi Netlify
@app.route("/api/")
def home():
    return jsonify({"message": "Flask server is running via Netlify Function!"})

@app.route("/api/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    query = data.get("query", "")
    
    # Semua logika internal Anda di sini TIDAK PERLU DIUBAH
    ngram_results = ngram_LM(query, total_unigram, total_bigram, total_trigram, total_vocabulary)
    predictions = {kata: prob for kata, prob in ngram_results}
    relevance_scores = tf_idf([query.lower()])
    relevant_docs = []
    keywords = query.lower().split()
    for doc_name, score in relevance_scores.head(10).items():
        if score > 0:
            document_text = doc_map.get(doc_name, "")
            snippet = generate_snippet(document_text, query)
            relevant_docs.append({
                "document": doc_name,
                "score": round(score, 5),
                "snippet": snippet
            })
    final_result = {
        "predictions": predictions,
        "documents": relevant_docs
    }
    return jsonify(final_result)

@app.route("/api/build", methods=["POST"])
def api_build():
    build_index()
    return jsonify({"status": "ok", "message": "Index berhasil dibuat / diperbarui"})

# --- Perubahan Paling Penting ---
# Hapus 'if __name__ == "__main__":' dan tambahkan fungsi handler
def handler(event, context):
    """
    Fungsi ini akan dipanggil oleh Netlify untuk setiap permintaan.
    serverless_wsgi akan meneruskan permintaan itu ke aplikasi Flask Anda.
    """
    return serverless_wsgi.handle_request(app, event, context)