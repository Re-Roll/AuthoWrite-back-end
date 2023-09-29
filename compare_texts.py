import glob
from tensorflow import keras
import numpy as np
import gensim
from functions import get_vectors
import os
from docu_functions import process_file

# initial folder path
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# load models
word2vec_model = gensim.models.Word2Vec.load(BASE_DIR+'/model_files/word2vec_model.model')
base_network = keras.models.load_model(BASE_DIR+"/model_files/base_network.h5", compile=False)
clf_network = keras.models.load_model(BASE_DIR+"/model_files/clf_network.h5", compile=False)

def compare_final_texts(known_text: list[str], unknown_text: list[str]) -> float:
    '''Compares a list of known texts to an unknown text and returns a score'''

    # get word vectors using w2v model & style vectors
    known_vec, known_w2v, known_style = get_vectors(known_text, word2vec_model)
    unknown_vec, unknown_w2v, unknown_style = get_vectors(unknown_text, word2vec_model)
    
    # create dictionary to compare style vectors between known and unknown texts
    style_dict = {key: [known_style[key], unknown_style[key]] for key in known_style.keys()}
    w2v_dist = np.linalg.norm(known_w2v - unknown_w2v, axis=0)  # word vector distances
    style_dict['w_sim'] = 100*w2v_dist
    
    # use word vectors to get feature vectors using base network model
    known_feature_vectors = base_network.predict(np.array(known_vec), verbose=0)
    unknown_feature_vectors = base_network.predict(np.array(unknown_vec), verbose=0)

    # get representations
    author_representation = np.mean(known_feature_vectors, axis=0)
    unknown_representation = np.mean(unknown_feature_vectors, axis=0)

    # use representations to get prediction using clf network model
    my_pred = clf_network.predict(np.array([np.concatenate((author_representation, unknown_representation), axis=None)]))

    return my_pred[0][0], style_dict

def compare_string_texts(known_text: str, unknown_text: str) -> float:
    '''Compares a string of a known text to an unknown text and returns a score'''
    return compare_final_texts([known_text], [unknown_text])

def compare_list_texts(known_texts: list[str], unknown_text: str) -> float:
    '''Compares a list of known texts to an unknown text and returns a score'''
    return compare_final_texts(known_texts, [unknown_text])

def compare_mix_texts(known_files, known_texts: list[str], unknown_file = None, unknown_text: str = None) -> float:
    '''Compares a mix of known texts and files to an unknown text and returns a score'''
    # initial check if known texts and files were provided
    if (not known_texts and not known_files) or (len(known_texts) == 0 and len(known_files) == 0):
        return 2, None
    
    if len(known_files) > 0:
        known_texts += [process_file(known_file) for known_file in known_files]  # add known texts from files
    known_texts = [text for text in known_texts if (text and not text.isspace())]  # remove empty texts
    known_texts = list(dict.fromkeys(known_texts))  # remove duplicates
    
    # check if known texts were provided
    if len(known_texts) == 0:
        return 2, None
    
    # check if unknown text was provided
    if unknown_file:
        unknown_text = process_file(unknown_file)
    elif not unknown_text:
        return 3, None
    
    # make sure unknown text is not empty or just whitespaces
    if unknown_text.isspace():
        return 3, None
    
    return compare_final_texts(known_texts, [unknown_text])