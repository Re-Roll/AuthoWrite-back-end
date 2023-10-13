'''
Code used to preprocess texts and extract features from them created by Eduardo Oliveira and his team.
Edited by Saaiq to use text instead of texts in the usecase
'''

import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

w2v_vector_size = 300

def preprocess_text(text):
    """
    Preprocess a given text by tokenizing, removing punctuation and numbers,
    removing stop words, and lemmatizing.

    Args:
        text (str): The text to preprocess.

    Returns:
        list: The preprocessed text as a list of tokens.
    """
    if not isinstance(text, str):
        text = str(text)

    # Tokenize the text into words
    tokens = word_tokenize(text.lower())

    # Remove punctuation and numbers
    table = str.maketrans('', '', string.punctuation + string.digits)
    tokens = [word.translate(table) for word in tokens]

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if (not word in stop_words) and (word != '')]

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens

def convert_text_to_vector(text, model):
    """
    Convert a list of texts into their corresponding word2vec vectors
    """
    words = preprocess_text(text)
    vector = np.sum([model.wv[word] for word in words if word in model.wv], axis=0)
    word_count = np.sum([word in model.wv for word in words])
    
    if word_count != 0:
        vector /= word_count
    else:
        vector = np.zeros(w2v_vector_size)

    return vector

def count_punctuations(text):
  """
  Count the frequency of different punctuations in the texts
  """
  # Define punctuations to count
  punctuations = set(['.', ',', ';', ':', '!', '?', '-', '(', ')', '\"', '\'', '`', '/'])

  # Initialize dictionary to count punctuations
  punctuations_count = {p: 0 for p in punctuations}

  # Count punctuations in text_list
  for char in text:
    if char in punctuations:
        punctuations_count[char] += 1

  # Return list of punctuation counts
  return list(punctuations_count.values())

def analyze_sentence_lengths(sentences):
  """
  Analyze the lengths of sentences
  """
  sentence_lengths = [len(sentence.split()) for sentence in sentences]
  average_length = np.mean(sentence_lengths)  #*
  count_over_avg = np.sum([length > average_length for length in sentence_lengths])
  count_under_avg = np.sum([length < average_length for length in sentence_lengths])
  count_avg = len(sentence_lengths) - count_over_avg - count_under_avg

  return [count_over_avg, count_under_avg, count_avg, average_length]

def analyze_words(text):
    """
    Analyze the words used in the texts
    """
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    tokenized = word_tokenize(text.lower())
    words = [lemmatizer.lemmatize(word) for word in tokenized if word not in stop_words]
    word_freq = nltk.FreqDist(words)
    rare_count = np.sum([freq <= 2 for word, freq in word_freq.items()])
    long_count = np.sum([len(word) > 6 for word in words])
    word_lengths = [len(word) for word in words]
    average_length = np.mean(word_lengths)
    count_over_avg = np.sum([length > average_length for length in word_lengths])
    count_under_avg = np.sum([length < average_length for length in word_lengths])
    count_avg = len(word_lengths) - count_over_avg - count_under_avg
    ttr = len(set(words)) / len(words) if words else 0                #*

    return [rare_count, long_count, count_over_avg, count_under_avg, count_avg, ttr]

def calculate_style_vector(text):
  """
  Calculate the style vector of the texts
  """
  punctuation_vec = count_punctuations(text)     # Punctuations stylistic features
  sentence_vec = analyze_sentence_lengths(nltk.sent_tokenize(text))  # Sentences stylistic features
  word_vec = analyze_words(text)                 # Words stylistic features
  word_count = len(text.split())
  
  vector = np.concatenate((punctuation_vec, sentence_vec, word_vec))
  if word_count > 0:
    vector /= word_count
    # dont divide some counts by word count
    vector[16] = sentence_vec[3]  # avg_sentence_length
    vector[22] = word_vec[5]      # ttr
  
  return vector, word_count

def get_vectors(texts, w2v_model):
  """
  Create the word2vec vectors and style vectors of the texts,
  Edited by Saaiq to output style vector information
  """
  res = []
  
  # headers for every key in style dictionary
  style_headers = (
      '.', ',', ';', ':', '!', '?', '-', '(', ')', '\"', '\'', '`', '/',
      'sentences_over_avg', 'sentences_under_avg', 'sentences_avg_length', 'avg_sentence_length',
      'rare_word_count', 'long_word_count', 'words_over_avg_length', 'words_under_avg_length', 'words_avg_length', 'ttr',
      'word_count'
  )
  style_dict = {key: [] for key in style_headers}
  
  for text in texts:
    w2v_vec = convert_text_to_vector(text, w2v_model)
    style_vec, word_count = calculate_style_vector(text)
    
    # input style vector information into style dictionary
    for i, header in enumerate(style_headers):
        if header == "word_count":
            style_dict[header].append(word_count)
        else:
            style_dict[header].append(style_vec[i])
    
    res.append(np.concatenate((w2v_vec, style_vec), axis=None))
  
  # convert to mean of style vectors
  style_dict = {key: np.median(value) for key, value in style_dict.items()}

  return res, w2v_vec, style_dict
