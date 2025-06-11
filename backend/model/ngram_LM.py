from model.normalize import normalize

def ngram_LM(query, total_unigram, total_bigram, total_trigram, total_vocabulary, top_k=5):
    stem_query = normalize(query)

    n = len(stem_query)
    k = 0.5
    v = total_vocabulary
    if n >= 2:
        w1, w2 = stem_query[-2], stem_query[-1]
        candidates = {
            t3: (cnt + k) / (total_bigram.get((w1, w2), 1) + (k * v))
            for (t1, t2, t3), cnt in total_trigram.items() if t1 == w1 and t2 == w2
        }
        if candidates:
            return sorted(candidates.items(), key=lambda x: x[1], reverse=True)[:top_k]

        candidates = {
            b2: (cnt + k) / (total_unigram.get(w2, 1) + (k * v))
            for (b1, b2), cnt in total_bigram.items() if b1 == w2
        }
        if candidates:
            return sorted(candidates.items(), key=lambda x: x[1], reverse=True)[:top_k]

        return total_unigram.most_common(top_k)

    elif n == 1:
        w = stem_query[0]
        candidates = {
            b2: (cnt + k) / (total_unigram.get(w, 1) + (k * v))
            for (b1, b2), cnt in total_bigram.items() if b1 == w
        }
        if candidates:
            return sorted(candidates.items(), key=lambda x: x[1], reverse=True)[:top_k]

        return total_unigram.most_common(top_k)

    else:
        return total_unigram.most_common(top_k)
