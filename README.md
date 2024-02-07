# Fill and Expand Bigrams
 A program for taking a list of pre-processed bigrams and filling in stopwords and prefixes/suffixes for use as completed keywords.

### Summary
 
This program uses existing data to fill in stop word gaps left by WordPPR's bigrams. It takes a .xlsx file of bigrams from WordPPR, existing files for each issue, and it outputs a list of all possible n-grams with their frequencies.
 
You will find the following files in this project folder:
1. **stopwords.txt**: a list of the most common English stop words; feel free to add more or modify
2. **data**: a folder which will contain the different .csv files containing the news or social media data
3. **bigrams.xlsx**: a .csv file which will contain all bigrams of interest and their corresponding issue categories
4. **keywords.xlsx**: a list of pre-existing seed keywords (to avoid duplicates)
5. **find_stopwords.py**: the program that will output the n-grams and frequencies

### Usage Guide
 
Here are the steps that you need to take to run the program:
1. Install the Python package "pandas" if not already installed
2. Move all .csv files containing text data for each issue category into the data folder
3. Fill out bigrams.xlsx for all bigrams of interest (under the "bigram" column)
4. Add any existing keywords to keywords.txt
5. Double-click find_stopwords.py to run the program


### Expected Output
 
After it finishes running, the program will output a file called Output.txt in the program directory. This file will contain all possible n-grams containing stop words between the two bigram words with corresponding frequencies, as well as potential preceeding/proceeding words.
