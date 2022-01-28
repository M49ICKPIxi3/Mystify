import pronouncing

import math
import random


def word_similarity(word_a, word_b):
    """
    Finds the similarity of two words.

    :param word_a: The first word to be compared.
    :param word_b: The second word to be compared.
    :return: A float representing the cosine similarity of the two words.
    """
    # Get the set of characters in each word.
    set_a = set(word_a)
    set_b = set(word_b)

    # Find the number of unique characters in each word.
    num_unique_chars_a = len(set_a)
    num_unique_chars_b = len(set_b)

    # Find the number of characters that are shared between the two words.
    num_shared = len(set.intersection(set_a, set_b))

    # Calculate the similarity.
    similarity = float(num_shared / (num_unique_chars_a * num_unique_chars_b))

    return similarity


"""def cosine_similarity(word_a, word_b):

    Finds the cosine similarity of two words.

    :param word_a: The first word to be compared.
    :param word_b: The second word to be compared.
    :return: A float representing the cosine similarity of the two words.


    # Get the set of all letters that are in both word_a and word_b.
    shared_letters = set(word_a).intersection(set(word_b))

    # Calculate the numerator for cosine similarity.
    numerator = 0

    # Calculate the denominator for cosine similarity.
    denominator = 0

    # Iterate over each shared word and add its contribution to the numerator and denominator.
    for shared_letter in shared_letters:
        str(word_a).count(shared_letter)
        numerator += (word_a.  * word_b[shared_letter])
        denominator += (word_a[shared_letter] ** 2) + (word_b[shared_letter] ** 2)
        denominator = math.sqrt(denominator)

    return numerator / denominator"""


def least_similar(words, word):
    """
    Find the least similar word from a list of words.

    :param words: A list of words to compare.
    :param word: The word to compare against the list.
    :return: The least similar word from the list.
    """
    return min(words, key=lambda x: word_similarity(word, x))

class RhymingApi(object):
    num_rhymes = 10

    def get_rhymes_for_word(self, word, num_rhymes=10):
        # TODO: Use a modified similarity metric to find the most diverse set of rhymes
        rhymes = set(pronouncing.rhymes(word)) # For now, using a random selection of rhymes
        if len(rhymes) == 0:
            return []
        elif len(rhymes) < num_rhymes:
            return list(rhymes)
        else:
            return random.choices(list(rhymes), k=num_rhymes)




def main():

    rhyming_api = RhymingApi()
    print(rhyming_api.get_rhymes_for_word(word='test'))


    #user_site = get_user_site()
    stop_here = ''

    #inspiration_words = ['lovely', 'pretty', 'sweet', 'joy']

    #print(pronouncing.rhymes('mary'))


if __name__ == '__main__':
    main()
