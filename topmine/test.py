import re
import string
import phrase_mining as pm

if __name__ == '__main__':
    splits = r'(?:\d[,.:]|[^,.:])*(?:[,.:]|$)'
    table = {ord(c): None for c in string.punctuation}
    table[ord('\n')] = ' '
    with open('example_document.txt', 'r') as f:
        document = re.findall(splits, f.read())
    corpus = [x.translate(table).lower().split(' ') for x in document]
    corpus = [[y for y in x if y != ''] for x in corpus]
    counter = pm.phrase_frequency(corpus, min_support=0)
    l = sum([len(d) for d in corpus])
    document = corpus[405]
    result = pm.segment_document(
        document=document, threshold=3, counter=counter, l=l)
    print(result)
