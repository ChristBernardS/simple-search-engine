import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

def normalize(text: str):
    ''' 
    1. Lowercase
    2. Remove non-alphanumeric characters
    3. Tokenize
    4. Remove Indonesian stopwords
    5. Stem tokens
    '''
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('indonesian'))
    filtered = [w for w in tokens if w not in stop_words and (w.isalpha() or w.isalnum())]
    stemmed = [stemmer.stem(w) for w in filtered]
    return stemmed