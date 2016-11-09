import re
import phrase_mining as pm

if __name__ == '__main__':
    splits = r'(?:\d[,.]|[^,.])*(?:[,.]|$)'
    with open('example_document.txt', 'r') as f:
        document = re.findall(splits, f.read())
    corpus = [x.split(' ') for x in document]
    print(corpus[0])
    print(corpus[1])
