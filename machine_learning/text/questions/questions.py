import nltk
import sys
import os
import string
import numpy as np

FILE_MATCHES = 1
SENTENCE_MATCHES = 2


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    corp_dict = {}
    filenames = sorted(os.listdir(f"{directory}{os.sep}"))
    for file in filenames:
        with open(f"{directory}{os.sep}{file}", 'r') as article:
            corp_dict[file] = article.read()

    return corp_dict



def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenized_list = []
    for word in nltk.word_tokenize(document.lower()):
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("russian"):
            tokenized_list.append(word)

    return tokenized_list


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words_idf = {}
    for doc_name in documents:
        for word in documents[doc_name]:
            count = 0
            for key in documents:
                if word in documents[key]:
                    count += 1
            idf = np.log(len(documents)/count)
            words_idf[word] = idf
    return words_idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    #tokenize query
    #if word in query appears in file dict count tf-idf
    #sum all tf-idf for query
    matching_dict = {x: 0 for x in files}
    for word in query:
        for file in files:
            if word in files[file]:
                tf =(files[file].count(word))
                tf_idf = tf*idfs[word]
                matching_dict[file] += tf_idf

    filenames = sorted(list(matching_dict.keys()), key = lambda x: matching_dict[x], reverse = True)
    return filenames[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    matching_dict = {x: 0 for x in sentences}
    count = 0
    for sentence in sentences:
        count = 0
        idf = 0
        for word in query:
            if word in sentences[sentence]:
                count += 1
                idf += idfs[word]
        qtd = count/len(sentences[sentence])
        matching_dict[sentence] = (idf, qtd)

    sentence_list = sorted(list(matching_dict.keys()), key = lambda x: (-1*matching_dict[x][0], -1*matching_dict[x][1]))

    return sentence_list[:n]



if __name__ == "__main__":
    main()
