"""
Student code for Word Wrangler game
"""

import urllib2
import SimpleGUICS2Pygame.codeskulptor as codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    sorted_list = []
    for item in list1:
        if not item in sorted_list:
            sorted_list.append(item)
    return sorted_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    if len(list1) == 0:
        return list2
    if len(list2) == 0:
        return list1
    interstction = []
    for item in list1:
        if item in list2:
            interstction.append(item)
    return interstction

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in both list1 and list2.

    This function can be iterative.
    """
    result = []
    eli, elj = 0, 0
    while eli < len(list1) and elj < len(list2):
        if list1[eli] <= list2[elj]:
            result.append(list1[eli])
            eli += 1
        else:
            result.append(list2[elj])
            elj += 1
    if eli == len(list1):
        result.extend(list2[elj:])
    else:
        result.extend(list1[eli:])
    return result


def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    len_lst = len(list1)
    if len_lst > 1:
        sort1 = merge_sort(list1[0:len_lst/2])
        sort2 = merge_sort(list1[len_lst/2:])
        return merge(sort1, sort2)
    else:
        return list1

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if word == "":
        return [""]
    first = word[0]
    rest = word[1:]
    rest_strings = gen_all_strings(rest)
    tmp = rest_strings[:]
    for letter in rest_strings:
        for idx in range(len(letter)+1):
            item = letter[:idx] + first + letter[idx:]
            tmp.append(item)
    return tmp


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    words = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        words.append(line[:-1])
    return words

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
