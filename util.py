import pickle

def load_data(filename):
    with open(filename + '.pickle', 'rb') as f:
        return pickle.load(f)
    
def save_data(filename, obj):
    with open(filename + '.pickle', 'wb') as f:
        return pickle.dump(obj, f)
