import pickle
import os
from django.conf import settings

def classify(text):
    path = os.path.join(settings.MEDIA_ROOT, 'files/fitted_classifier.pkl')
    with open(path, 'rb') as file:
        classifier = pickle.load(file)
        predicted_labels = classifier.predict([text])
    
    return predicted_labels