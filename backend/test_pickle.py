import pickle

with open('src/index/total_vocabulary.pkl', 'rb') as f:
    data = pickle.load(f)

print(data)