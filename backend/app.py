from flask import Flask, request, jsonify
from flask_cors import CORS
from model.ngram_LM import ngram_LM
from model.build_index import build_index
from model.load_index import load_index

app = Flask(__name__)
CORS(app)

# Load model saat startup
try:
    counts_per_doc, total_unigram, total_bigram, total_trigram, total_vocabulary = load_index()
except FileNotFoundError:
    print(">> File index tidak ditemukan. Membuat index baru …")
    counts_per_doc, total_unigram, total_bigram, total_trigram, total_vocabulary = build_index()

@app.route("/")
def home():
    return jsonify({"message": "Flask server is running!"})

@app.route("/predict", methods=["POST"])
def api_predict():
    data = request.get_json()
    query = data.get("query", "")
    result = ngram_LM(query, total_unigram, total_bigram, total_trigram, total_vocabulary)
    predictions = {'predictions' : {}}
    for idx, (kata, prob) in enumerate(result):
        predictions['predictions'].update({f"{kata}":prob})
    return jsonify(predictions)

@app.route("/build", methods=["POST"])
def api_build():
    build_index()
    return jsonify({"status": "ok", "message": "Index berhasil dibuat / diperbarui"})

if __name__ == "__main__":
    app.run(debug=True)