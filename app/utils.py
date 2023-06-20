import os
import pickle
import pandas as pd
from django.conf import settings
import openai
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config.get("OPENAI_API_KEY")


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

def split_string(input_string):
    # input a law case as a long string
    # @return a string array [law case part 1, law case part 2, law case part 3 .....]
    
    n = 2000 
    return [input_string[i: i + n] for i in range(0, len(input_string), n)]
    

def summarizerHelper(str_array):
    if (len(str_array) <= 1) :
        user_input = str_array[0]
        prompt = f"As a lawyer, summarize this text in professional way for other lawyer to refer to the law case as a third view.: {user_input}"

        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=1000
        )
        return res["choices"][0]["text"]
    else:
        # more than one element in array
        # we need to summarize everything in the array
        # then join back into a string
        # then split into array and call recursively
        output=""
        for item in str_array:
            prompt =  f"As a lawyer, summarize this text in professional way for other lawyer to refer to the law case as a third view.: {item}"
            res = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.5,
                max_tokens=1000
            )
            output += res["choices"][0]["text"]
        
        ## split into string array (luke function) 
        new_array = split_string(output)
        return summarizerHelper(new_array)

        
# Luke only need to user this function
# @return a summary of a law case
# You have to "manually" get a law case, input this function to get the summary
def summarize_law_case(input):
    ## input here will be law case
    
    ## then here do split string
    arr = split_string(input)
    
    ## then do summarizer here
    return summarizerHelper(arr)