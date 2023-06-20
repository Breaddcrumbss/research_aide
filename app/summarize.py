import pandas as pd
from utils import summarizerHelper, summarize_law_case, find_cases
import openai 
from dotenv import dotenv_values

config = dotenv_values(".env")
openai.api_key = config.get("OPENAI_API_KEY")

# this is what we should input in the search bar as example to get the cases we summarised
prompt = '''two parties have signed a contract, but it was agreed that a guarantor must also sign the contract for it to be valid. 
            Issue is whether the contract is still valid without the signature of the guarantor.'''

df = pd.read_csv('../media/files/split_cleaned_data.tsv', sep='\t', converters={'Case Text': pd.eval})
df = df.drop_duplicates(subset='Name')
matches = df[df['Simple Catchwords'] == 'contract '][['Name', 'Case Text']].head(3)

print(matches)
cases = []          #list of dicts with case text
for index, row in matches.iterrows():
    case_info = {}
    case_info['name'] = row['Name']
    case_info['text'] = row['Case Text']
    cases.append(case_info)

# # CG can change these parameters
case_index = 2      # index out of 5 of the case texts
para = 3            # to control until which paragraph to summarise

# # Input for the summarise function (str array). I removed the split string call in the summarize function because already split
# # Print case to test see if its the correct structure
case = cases[case_index]['name']

for case in cases:
    print(case['name'])
# print(len(case))
# print("======")
# print(case[0])
# print("========")
# print(summarize_law_case(case))


# # below for testing
# print(case)
# output = summarize_law_case(case)
# print(output)

# # When ready to enter all 5 summaries, append to following list
# summary_text = []     # put each summary of the case into a list, following order of index
# case_name = [case['name'] for case in cases]

# # Creates dataframe for each case summary with case name
# case_summaries = [case_name, summary_text]
# summary_df = pd.DataFrame(case_summaries).transpose()
# summary_df.columns = ['Name', "Summary"]

# # Save to files folder
# summary_df.to_csv('../media/files/.tsv', encoding='UTF-8', sep='\t')