library(readxl)

#=======================================================
#
# Configuration
#
#=======================================================

# filepath/filename containing bigrams
# inferred structure: bigram column, issue column
bigrams <- readxl("bigrams.xlsx")

# change if using different text columns for one of the datasets
text_column <- "Mention Content"
