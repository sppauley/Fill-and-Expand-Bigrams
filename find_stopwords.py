import pandas as pd
import os
import re
import filtering_rules

#=======================================================
#
# Configuration
#
#=======================================================

# filepath/filename containing bigrams
# inferred structure: bigram column, issue column
bigrams = pd.read_excel('bigrams.xlsx')

# change if using different text columns for one of the datasets
text_column = 'Mention Content'

# loads a shared set of stopwords from NLTK and spaCy
# kept in an external .txt file, feel free to modify with others
stopwords = open('stopwords.txt', 'r', encoding="utf-8").read()
stopwords = stopwords.split('\n')

# loads a set of prior keywords for comparison (to avoid duplicates)
keyword_list = open('keywords.txt', 'r', encoding="utf-8").read()
keyword_list = keyword_list.split(', ')

# uses regex and the list of stopwords to create a large regex pattern specifically for stopwords
# allows for up to quandrigrams
pattern = '(?:(?:'+'|'.join(stopwords)+')\s)*'

print([keyword for keyword in keyword_list])

#=======================================================
#
# Functions
#
#=======================================================

# function designed to take the raw text series and return a set of n-grams and counts
'''
Arguments:
text_series: takes a text column
bigram: for testing different bigrams, test them separately for clearer output
'''

def find_ngrams(text_series, bigram):

    # splits the bigram for easier processing
    bigram_tokens = bigram.split('_')

    # nested sub-function for iteration
    def get_ngrams(text):

        # finds all ngrams starting with the first bigram token and ending with the last
        # adds \w characters, since word PPR removes plurals 's' and verb endings like 'ed'
        ngrams = re.findall('((?:\w+\s)?('+bigram_tokens[0]+'\w*'+' '+pattern+bigram_tokens[1]+'\w*)'+'(?:\s\w+)?)', text)
        
        return ngrams

    # gets the full list, subsets to stopwords between and then full ngrams
    full_list = [get_ngrams(text.lower()) for text in text_series if type(text)==str]
    stopwords_between = [[entry[1] for entry in ngram_list] for ngram_list in full_list if type(ngram_list)==list]
    ngrams_extended = [[entry[0] for entry in ngram_list] for ngram_list in full_list if type(ngram_list)==list]

    # flattens the matrices
    ngrams_extended = sum(ngrams_extended, [])
    stopwords_between = sum(stopwords_between, [])

    # creates a set of counts for each, returns them in order
    output = pd.DataFrame({'stopwords':stopwords_between, 'ngrams':ngrams_extended})
    ngrams_sorted = output.groupby('ngrams').size().reset_index().rename(columns={0:'count'}).sort_values('count', ascending=False).head(20)
    stopwords_sorted = output.groupby('stopwords').size().reset_index().rename(columns={0:'count'}).sort_values('count', ascending=False).head(20)

    output = filtering_rules.combined_filter(output, stopwords_sorted, ngrams_sorted, bigram.replace('_',' '), keyword_list)

    return output

# function for filling the stopwords between bigrams
'''
Arguments:
text_filepath = filepath to the .csv file containing text (assumes prefixed with the issue category)
'''
def fill_bigrams(text_filepath):

    # imports the text file
    df = pd.read_csv(text_filepath)

    # checks the issue category
    issue_category = re.findall('data\/(\w+)_(?:news|social).csv', text_filepath)[0]

    # subsets bigrams to that issue category
    subset = bigrams[bigrams['issue_category']==issue_category]['bigram']

    # creates an empty dataframe for output
    print(('='*50) + '\n\nBigrams for file: ' + text_filepath + '\n\n')
    output = pd.DataFrame()
    
    # iterates through the bigrams, finds ngrams for each, concats to output
    for bigram in subset:
        if len(bigram.split('_'))>1:
            bigram_set = find_ngrams(df[text_column], bigram)
            print(bigram_set)
            output = pd.concat([output, bigram_set])

    output['issue'] = issue_category

    return output

#=======================================================
#
# Runtime (sets up and runs the program)
#
#=======================================================

# gets a list of files in the data folder for subsequent iteration
file_list = ['data/'+f for f in os.listdir('data') if os.path.isfile('data/'+f)]

# sets an empty dataframe for output
output_df = pd.DataFrame()

# iterates through the files and fills bigrams
for file in file_list:
    output_df = pd.concat([output_df, fill_bigrams(file)])

# writes the output to a .xlsx file
with pd.ExcelWriter('Output.xlsx') as writer:
    for issue in output_df['issue'].unique():
        output_df[output_df['issue']==issue].to_excel(writer, sheet_name = issue)

