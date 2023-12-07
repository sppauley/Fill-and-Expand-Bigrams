library(readxl)
library(readr)
library(stringr)

#=======================================================
#
# Configuration
#
#=======================================================

# filepath/filename containing bigrams
# inferred structure: bigram column, issue column
bigrams <- read_excel("bigrams.xlsx")

# change if using different text columns for one of the datasets
text_column <- "Mention Content"

# loads a shared set of stopwords from NLTK and spaCy
# kept in an external .txt file, feel free to modify with others
stopwords <- read_file("stopwords.txt")

# uses list of stopwords to create a large regex pattern
# allows for up to quandrigrams
pattern <- paste("(?:(?:", str_replace_all(stopwords, "\\n", "|"), ")\\s)*")

#=======================================================
#
# Functions
#
#=======================================================
