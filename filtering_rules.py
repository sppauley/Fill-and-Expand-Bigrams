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

# Rule 3 (also includes 2 by logic): checks if the bigram frequency is greater than or equal to 5
'''
Takes an argument for output dataframe
Returns true if passes check, else false
'''
def check_frequency(dataframe, frequency = 5):
    return dataframe.shape[0] >= frequency

# Rule 5a_: checks if the bigram with stopwords between can be captured by pre-existing keywords
'''
Takes an argument for the stopwords output and the full bigram .xlsx file
Returns filtered dataframe
'''
def filter_capture(stopwords_dataframe, keyword_list, frequency = 5):
    
    # filters dataframe based on frequency
    test_df = stopwords_dataframe[stopwords_dataframe['count'] >= frequency]

    '''
    Underlying function for use in lambdas
    Takes argument for stopword phrase
    Returns True if captured by keywords, else False
    '''
    def check_capture(phrase):
        return any([True if keyword in phrase else False for keyword in keyword_list])

    # applies and filters based on the capture check
    test_df['filter'] = test_df['stopwords_between'].apply(lambda x: check_capture(x))
    return test_df[test_df['filter']==False].drop(columns=['filter'])

#=======================================================
#
# Combined filtering functions
#
#=======================================================

'''
Uses a broader structure to combine the rules
Returns TRUE if the bigram should be included, else FALSE
'''
def combined_filter(dataframe, stopwords_dataframe, root_bigram, keyword_list):

    # creates the blank list
    output = []

    # include the base bigram IF the first fails and the second two pass
    if not check_in_keywords(root_bigram, keyword_list) and check_frequency(dataframe):
        output.append(root_bigram)

    

    return output

keyword_list = pd.DataFrame({'bigram':['one_two','three_four', 'one_three']})
df = pd.DataFrame({'stopwords_between':['one two', 'one nine two'], 'count':[6,7]})
print(filter_capture(df, keyword_list))