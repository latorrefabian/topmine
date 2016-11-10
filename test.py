import re
import string
from topmine import phrase_mining as pm
import argparse
import pickle

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='test topmine on a book')
    parser.add_argument('-t', '--threshold', type=int)
    parser.add_argument('-d', '--document', type=int)
    args = parser.parse_args()
    splits = r'(?:\d[,.:]|[^,.:])*(?:[,.:]|$)'
    table = {ord(c): None for c in string.punctuation}
    table[ord('\n')] = ' '
    with open('example_document.txt', 'r') as f:
        document = re.findall(splits, f.read())
    corpus = [x.translate(table).lower().split(' ') for x in document]
    corpus = [[y for y in x if y != ''] for x in corpus]
    counter = pm.phrase_frequency(corpus, min_support=0)
    l = sum([len(d) for d in corpus])
    result = pm.segment_document(
        document=corpus[args.document], threshold=args.threshold,
        counter=counter, l=l)
    print(result)
