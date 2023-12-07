import pandas as pd
import os
import re

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
stopwords = open('stopwords 2.txt', 'r', encoding="utf-8").read()
stopwords = stopwords.split('\n')

# uses regex and the list of stopwords to create a large regex pattern specifically for stopwords
# allows for up to quandrigrams
pattern = '(?:(?:'+'|'.join(stopwords)+')\s)*'

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
        ngrams = re.findall('(\w+\s)?('+bigram_tokens[0]+'\w*'+' '+pattern+bigram_tokens[1]+')\w*'+'(\s\w+)?', text)
        
        return ngrams

    #ngram_list = [get_ngrams(text) for text in text_series if type(text)==str]
    

    full_list = [get_ngrams(text.lower()) for text in text_series if type(text)==str]

    words_before = [[entry[0] for entry in ngram_list] for ngram_list in full_list if type(ngram_list)==list]
    stopwords_between = [[entry[1] for entry in ngram_list] for ngram_list in full_list if type(ngram_list)==list]
    words_after = [[entry[2] for entry in ngram_list] for ngram_list in full_list if type(ngram_list)==list]

    # flattens the matrices
    words_before = sum(words_before, [])
    stopwords_between = sum(stopwords_between, [])
    words_after = sum(words_after, [])

    # creates a set of counts for each, returns them in order as a string
    output = pd.DataFrame({'words before':words_before, 'words after':words_after, 'stopwords between':stopwords_between})
    output_stopwords = output.groupby('stopwords between').size().reset_index().rename(columns={0:'count'}).sort_values('count', ascending=False).head(20)
    output_before = output.groupby('words before').size().reset_index().rename(columns={0:'count'}).sort_values('count', ascending=False).head(10)
    output_after = output.groupby('words after').size().reset_index().rename(columns={0:'count'}).sort_values('count', ascending=False).head(10)

    # formats as a string
    if output.shape[0]>0:
        total = 'total occurrences: '+str(output.shape[0])
        output_stopwords = re.sub('\n\d+', '\n', str(output_stopwords))
        output_before = re.sub('\n\d+', '\n', str(output_before))
        output_after = re.sub('\n\d+', '\n', str(output_after))
        output = bigram+'\n'+total + '\n\n'+ output_stopwords + '\n\n' + output_before + '\n\n' + output_after
    else:
        output = 'No occurrences for '+bigram

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

    # sets a formatted blank output string
    output = ('='*50) + '\n\nBigrams for file: ' + text_filepath + '\n\n'
    print(output)
    
    # iterates through the bigrams, finds ngrams for each, concats to output
    for bigram in subset:
        if len(bigram.split('_'))>1:
            ngrams = find_ngrams(df[text_column], bigram)
            print(ngrams+'\n\n')
            output = output + ngrams + '\n\n'

    return output

#=======================================================
#
# Runtime (sets up and runs the program)
#
#=======================================================

# gets a list of files in the data folder for subsequent iteration
file_list = ['data/'+f for f in os.listdir('data') if os.path.isfile('data/'+f)]

# sets a default text string for later output into a file
text_output = ''

# iterates through the files and fills bigrams
for file in file_list:
    text_output = text_output + fill_bigrams(file)

# writes the output to a .txt file
with open("Output.txt", "w") as text_file:
    text_file.write(text_output)

