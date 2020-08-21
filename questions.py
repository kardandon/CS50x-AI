import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


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
    contents = dict()
    import os
    path = os.path.join(".", f"{directory}")
    for file in os.listdir(path):
        with open(os.path.join(path, file), "r", encoding="utf8") as f:
            contents[file[:-4]] = f.read()
    return contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = [word.lower() for word in nltk.word_tokenize(document)]

    stopwords = nltk.corpus.stopwords.words("english")
    import string
    punct = [x for x in string.punctuation]
    return [word for word in tokens if word not in stopwords and word not in punct]


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    num = len(documents)
    presence = dict()
    idfs = dict()
    import math
    for doc in documents:
        for word in set(documents[doc]):
            try:
                presence[word] += 1
            except KeyError:
                presence[word] = 1
    for word in presence:
        idfs[word] = math.log(num / presence[word])
    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = dict()
    for file in files:
        tfidfs[file] = 0
        num = len(files[file])
        for word in query:
            if word in files[file]:
                freq = files[file].count(word)
            else:
                freq = 1
            try:
                idf = idfs[word]
            except KeyError:
                idf = 1
            tfidfs[file] = idf * freq
    lst = sorted(tfidfs, key=tfidfs.get, reverse=True)
    return lst[:n]
            

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    stats = {}
    for sentence in sentences:
        stats[sentence] = dict()
        stats[sentence]["idf"] = 0
        stats[sentence]["count"] = 0
        num = len(sentences[sentence])
        for word in query:
            if word in sentences[sentence]:
                stats[sentence]["idf"] += idfs[word]
                stats[sentence]["count"] += 1
        stats[sentence]["QTD"] = stats[sentence]["count"] / num
    lst = sorted(stats.keys(), key=lambda s: (stats[s]["idf"], stats[s]["QTD"]), reverse=True)
    return lst[:n]


if __name__ == "__main__":
    main()
