import os

def read_corpus():
    '''
    Read all .txt files under data_path.
    Returns a tuple of (contens, filenames)
    '''
    DATA_PATH = r"src/corpus/"
    news_list = []
    file_names = sorted([fn for fn in os.listdir(DATA_PATH) if fn.lower().endswith('.txt')])
    for fn in file_names:
        path = os.path.join(DATA_PATH, fn)
        with open(path, 'r', encoding='utf-8') as f:
            contain = f.read()
            news_list.append(contain)
    return news_list, file_names