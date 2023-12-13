import pandas as pd

#=======================================================
#
# Functions for each filtering rule
#
#=======================================================

# Rule 1: checks if the bigram is already in the full keywords list
'''
Takes an argument for the root bigram and the full bigram .xlsx file
Returns true if passes check, else false
'''
def check_in_keywords(root_bigram, keyword_list):
    return root_bigram in keyword_list

# Rule 2 & 3: checks if the bigram frequency is greater than or equal to 5
'''
Takes an argument for output dataframe
Returns true if passes check, else false
'''
def check_frequency(dataframe, frequency = 5):
    return dataframe.shape[0] >= frequency

# Rule 5 & 6: checks if the bigram with stopwords between can be captured by pre-existing keywords
'''
Takes an argument for the stopwords output and the full bigram .xlsx file
Returns filtered dataframe
'''
def filter_capture(narrowed_dataframe, phrase_column, keyword_list, frequency = 5):
    
    # filters dataframe based on frequency
    test_df = narrowed_dataframe[narrowed_dataframe['count'] >= frequency]

    '''
    Underlying function for use in lambdas
    Takes argument for stopword phrase
    Returns True if captured by keywords, else False
    '''
    def check_capture(phrase):
        return any([True if keyword in phrase else False for keyword in keyword_list])

    # applies and filters based on the capture check
    test_df['filter'] = test_df[phrase_column].apply(lambda x: check_capture(x))
    test_df = test_df.rename(columns={phrase_column:'keyword'})
    return test_df[test_df['filter']==False].drop(columns=['filter'])

# Rule 6: checks if the bigram with words before and/or after can be captured by pre-existing keywords
'''
Takes an argument for the stopwords output and the full bigram .xlsx file
Returns filtered dataframe
'''
def filter_order(test_dataframe, keyword_list, frequency = 5):
    return test_dataframe[test_dataframe['count'] >= frequency]

#=======================================================
#
# Combined filtering functions
#
#=======================================================

'''
Uses a broader structure to combine the rules
Returns TRUE if the bigram should be included, else FALSE
'''
def combined_filter(dataframe, stopwords_dataframe, extension_dataframe, root_bigram, keyword_list): 

    # creates the blank dataframe
    output = pd.DataFrame({'keyword':[], 'count':[], 'type':[]})

    # include the base bigram IF the first fails and the second two pass
    if not check_in_keywords(root_bigram, keyword_list) and check_frequency(dataframe):
        output = pd.concat([output, pd.DataFrame({'keyword':[root_bigram], 'count':[dataframe.shape[0]], 'type':['root bigram']})])

    # filters the stopwords
    stopwords_filtered = filter_capture(stopwords_dataframe, 'stopwords', keyword_list)
    if stopwords_filtered.shape[0] > 0:
        stopwords_filtered['type'] = 'stopwords filled'
        output = pd.concat([output, stopwords_filtered])

    # filters the extended phrases
    extensions_filtered = filter_capture(extension_dataframe, 'ngrams', keyword_list)
    if extensions_filtered.shape[0] > 0:
        extensions_filtered['type'] = 'extended ngram'
        output = pd.concat([output, extensions_filtered])

    return output