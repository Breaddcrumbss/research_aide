import os
import pickle
import pandas as pd
from django.conf import settings


def classify(text):
    path = os.path.join(settings.MEDIA_ROOT, 'files/fitted_classifier.pkl')
    with open(path, 'rb') as file:
        classifier = pickle.load(file)
        predicted_labels = classifier.predict([text.lower()])[0]
    
    return predicted_labels

def find_cases(label):
    df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'files/split_cleaned_data.tsv'), sep='\t')
    matches = df[df['Simple Catchwords'] == label][['Name', 'URL', 'Case Text']].head(5)
    cases = []
    for index, row in matches.iterrows():
        case_info = {}
        case_info['name'] = row['Name']
        case_info['URL'] = row['URL']
        case_info['text'] = row['Case Text']
        cases.append(case_info)
    
    return cases

