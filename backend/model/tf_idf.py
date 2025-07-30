import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from model.read_corpus import read_corpus

def tf_idf(query):
    # Mengambil query string utuh dan memecahnya menjadi kata kunci
    full_query_str = query[0]
    keywords = full_query_str.lower().split()

    berita_list, file_names = read_corpus()
    
    vectorizer = TfidfVectorizer(smooth_idf=True, use_idf=True)
    doc_tfidf_matrix = vectorizer.fit_transform(berita_list)

    query_tfidf_vector = vectorizer.transform([full_query_str])
    cos_sim = cosine_similarity(query_tfidf_vector, doc_tfidf_matrix).flatten()

    relevance_scores = pd.Series(cos_sim, index=file_names)

    if len(keywords) > 1:
        boost_value = 0.1
        
        for i, doc_text in enumerate(berita_list):
            doc_lower = doc_text.lower()
            
            all_keywords_present = True
            for keyword in keywords:
                if not re.search(r'\b' + re.escape(keyword) + r'\b', doc_lower):
                    all_keywords_present = False
                    break
            
            if all_keywords_present:
                doc_name = file_names[i]
                relevance_scores[doc_name] += boost_value

    if relevance_scores.max() == 0:
        existing_keywords = [word for word in keywords if word in vectorizer.get_feature_names_out()]
        if existing_keywords:
            df_tfidf = pd.DataFrame(
                doc_tfidf_matrix.toarray(),
                index=file_names,
                columns=vectorizer.get_feature_names_out()
            )
            fallback_scores = df_tfidf[existing_keywords].sum(axis=1)
            return fallback_scores.sort_values(ascending=False)

    return relevance_scores.sort_values(ascending=False)