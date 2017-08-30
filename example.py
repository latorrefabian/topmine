from __future__ import print_function
from topmine import Corpus, TopmineTokenizer

corpus = Corpus(files=['topmine/corpus_example/1.txt'])
tokenizer = TopmineTokenizer(threshold=0.1)
tokenizer.fit(corpus=corpus)
print(tokenizer.transform_document('the people of the united states'))
