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
stopwords <- str_replace_all(stopwords, "\\n", "|")
pattern <- paste("(?:(?:", stopwords, ")\\s)*", sep = "")

#=======================================================
#
# Functions
#
#=======================================================

# takes the raw text series and return a set of n-grams and counts
#
#Arguments:
#text_series: takes a text column
#bigram: for testing different bigrams, test them separately for clearer output
#

find_ngrams <- function(text_series, bigram) {

  print(bigram)

  # splits the bigram for easier processing
  tokens <- as.list(strsplit(bigram, "_")[[1]])

  # nested sub-function for iteration
  get_ngrams <- function(text) {

    # finds all ngrams starting with first bigram token and ending with last
    # adds \w characters (word PPR removes plurals 's' and endings like 'ed')
    base <- paste(tokens[1], "\\w* ", pattern, tokens[2], sep = "")
    pattern_full <- paste("(\\w+\\s)?(", base, ")\\w*", "(\\s\\w+)?", sep = "")

    ngrams <- str_match(text, pattern_full)

    ngrams_output <- c()

    for (ngram in ngrams){
      ngrams_output <- c(ngrams_output, ngram)
    }
    return(ngrams_output)
  }

  words_before <- c()
  stopwords_between <- c()
  words_after <- c()

  for (text in text_series){
    if (typeof(text) == "character") {
      print('text')
      ngram_list <- get_ngrams(str_to_lower(text))
      words_before <- c(words_before, ngram_list[2])
      stopwords_between <- c(stopwords_between, ngram_list[3])
      words_after <- c(words_after, ngram_list[4])
    }
  }
  print(words_before)
  # creates a dataframe with counts for each
  df <- data.frame(
    words_before = words_before,
    stopwords_between = stopwords_between,
    words_after = words_after
  )

  stopwords_output <- sort(table(df$stopwords_between)[1:20], decreasing = TRUE)
  before_output <- sort(table(df$words_before)[1:10], decreasing = TRUE)
  after_output <- sort(table(df$words_after)[1:10], decreasing = TRUE)

  return(before_output)

}
find_ngrams(file["Mention.Content"], "gun_owner")

file = read.csv('data/gun_social.csv')
