import argparse
import re

import numpy as np


def get_bigram_counts(file_or_str, separator_regex=r'\W+'):
    """ Get bigram counts from a text file.

    Lowercases all words. Words are delimited by separator_regex (by default, any non-word characters). Separators are
    not included in the bigrams.

    :param file_or_str: File-like object to read text from (iterator should return lines) or a string
    :param separator_regex: By default, split on any non-word characters (\W+)
    :return: Tuple of (bigrams, bigram_counts), where bigrams is a numpy array of bigrams and bigram_counts is a numpy
    array of their counts, both sorted in descending order by count.
    """
    if isinstance(file_or_str, str):
        file_or_str = file_or_str.splitlines()

    words = []
    pattern = re.compile(separator_regex)

    for line in file_or_str:
        line_words = re.split(pattern, line.strip())  # can contain empty strings, e.g. if line ends with a separator
        words.extend((word.lower() for word in line_words if word != ''))

    bigrams = list(zip(words[:-1], words[1:]))
    bigrams, bigram_counts = np.unique(bigrams, return_counts=True, axis=0)
    desc_sorted_indices = np.argsort(bigram_counts)[::-1]

    return bigrams[desc_sorted_indices], bigram_counts[desc_sorted_indices]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get bigram counts from a text file')
    parser.add_argument('file', type=argparse.FileType('r'), help='Plaintext file to read')
    parser.add_argument('-n', '--num', type=int, default=10, help='Number of most frequent bigrams to print)')

    args = parser.parse_args()
    bigrams, bigram_counts = get_bigram_counts(args.file)

    for bigram, count in zip(bigrams[:args.num], bigram_counts[:args.num]):
        print(f'{bigram}: {count}')