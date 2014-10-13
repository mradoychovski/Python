"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import alg_project4_solution as student
else:
    import simpleplot
    import userXX_XXXXXXX as student
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list


############## Aplication 4 - Applications to genomics and beyond ##############
################################ Solution ######################################


def App4_Q1(scoring_matrix):
    """
    Compute local alignment of Human Eyeless Protein and
    Fruitfly Eyeless Protein sequenceces
    Return:
        Tuple of score and alignede sequences
        (score, alignedFruitflyEyelessProtein, alignedFruitflyEyelessProtein)
    """
    # Load files
    human = read_protein(HUMAN_EYELESS_URL)
    fruitfly = read_protein(FRUITFLY_EYELESS_URL)

    # Compute local alignement
    (score, aligned_human, aligned_fruitfly) = \
        student.local_alignment(human, fruitfly, scoring_matrix)

    return (score, aligned_human, aligned_fruitfly)


def App4_Q2(scoring_matrix):
    # Load Consensus PAM sequence
    consensus = read_protein(CONSENSUS_PAX_URL)

    # Compute local alignment from Q1
    (score, human, fruitfly) = App4_Q1(scoring_matrix)

    # Remove dashes from local aligned sequence
    dashless_human = [ch for ch in human if not ch == '-']
    dashless_fruitfly = [ch for ch in fruitfly if not ch == '-']

    # Compute global alignemnt
    human_consensus = student.global_alignment(
        dashless_human, consensus, scoring_matrix)
    fruitfly_consensus = student.global_alignment(
        dashless_fruitfly, consensus, scoring_matrix)

    # Compute percentage of elements that agree
    human_cons_agree = sum([1. for hmn, cons in zip(
        human_consensus[1], human_consensus[2]) if hmn != cons])
    fruitfly_cons_agree = sum([1. for ff, cons in zip(
        fruitfly_consensus[1], fruitfly_consensus[2]) if ff != cons])
    human_cons_per = human_cons_agree / len(human_consensus[1]) * 100.
    fruitfly_cons_per = fruitfly_cons_agree / len(fruitfly_consensus[1]) * 100.

    return human_cons_per, fruitfly_cons_per


# App4_Q4
def generate_null_distribution(seq_x,seq_y, scoring_matrix, num_trials):
    """
    Takes as input two sequences seq_x and seq_y, a scoring matrix
    scoring_matrix, and a number of trials num_trials. This function should
    return a dictionary scoring_distribution that represents an un-normalized
    distribution generated by performing the following process num_trials times:
      - Generate a random permutation rand_y of the sequence seq_y using
    random.shuffle().
      - Compute the maximum value score for the local alignment of seq_x and
    rand_y using the score matrix scoring_matrix.
      - Increment the entry score in the dictionary scoring_distribution by one.
    """
    pass


def App_Q5():
    pass


def App4_Q6():
    pass


def App4_Q7():
    pass


def App4_Q8():
    pass


if __name__ == "__main__":
    scoring_matrix = read_scoring_matrix(PAM50_URL)
    #print App4_Q1(scoring_matrix)
    print App4_Q2(scoring_matrix)
