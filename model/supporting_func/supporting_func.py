import pickle


#Saves model weights and biases
def save_model(trained_model):
    with open('trained_model.pickle', 'wb') as target:
        pickle.dump(trained_model, target)
    print("\nSaved model in trained_model.pickle\n")

#loads the appropriate pickle file
def load_model():
    with open('trained_model.pickle', 'rb') as target:
        trained_model = pickle.load(target)
    print("\nLoaded model in trained_model.pickle\n")
    return trained_model
