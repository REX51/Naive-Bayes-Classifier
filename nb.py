import time
start = time.time()
import nltk
import string
import pickle
import random
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import enchant
# from nltk.stem.wordnet import WordNetLemmatizer

# lemmatizer = WordNetLemmatizer()


#for positive reviews
with open('positive.txt','r') as fp:
    data_pos = fp.read().splitlines()

l = []
for line in data_pos:
    l.append(line.split(','))


random.shuffle(l)


pos_review = []
for w in l:
    for i in w:
        pos_review.append(word_tokenize(i))
        


for w in pos_review:
    for i in w:
        if i in stopwords.words("english"):
            w.remove(i)

            
for w in pos_review:
    for i in w:
        if len(i)<3:
            w.remove(i)

        
d = enchant.Dict("en_US")

for w in pos_review:
    for i in w:
        if d.check(i)==False:
            w.remove(i)
        else:
            continue



#for negative reviews
with open('negative.txt','r') as fn:
    data_neg = fn.read().splitlines()

n = []
for line in data_neg:
    n.append(line.split(','))
    
random.shuffle(n)
    
neg_review = []
for w in n:
    for i in w:
        neg_review.append(word_tokenize(i))
        


for w in neg_review:
    for i in w:
        if i in stopwords.words("english"):
            w.remove(i)

            
for w in neg_review:
    for i in w:
        if len(i)<3:
            w.remove(i)

        
d = enchant.Dict("en_US")

for w in neg_review:
    for i in w:
        if d.check(i)==False:
            w.remove(i)
        



mega_doc = []
for s in pos_review[:int(len(pos_review)*0.70)]:
        mega_doc.append(s)
    
len_pos = len(mega_doc)

for s in neg_review[:int(len(neg_review)*0.70)]:
        mega_doc.append(s)


mega_pos_review = mega_doc[:len_pos]
mega_neg_review = mega_doc[len_pos:]


vocab = set()

for s in mega_doc:
    for w in s:
        vocab.add(w)
        
vocab = list(vocab)


count_l_pos = {}
count_l_neg = {}

for w in vocab:
    counter = 0
    for s in mega_pos_review:
        counter += s.count(w)
    count_l_pos[w] = counter

for w in vocab:
    counter = 0
    for s in mega_neg_review:
        counter += s.count(w)
    count_l_neg[w] = counter

total_pos = 0
total_neg = 0

for key in count_l_pos:
    total_pos += count_l_pos.get(key)

for key in count_l_neg:
    total_neg += count_l_neg.get(key)

prob_pos_word = {}
prob_neg_word = {}

for key in vocab:
    prob = (count_l_pos.get(key)+1)/(total_pos+len(vocab)+1)
    prob_pos_word[key] = prob

for key in vocab:
    prob = (count_l_neg.get(key)+1)/(total_neg+len(vocab)+1)
    prob_neg_word[key] = prob

test_doc = []
for s in pos_review[:int(len(pos_review)*0.70)]:
    test_doc.append(s)
    
len_pos_test = len(test_doc)

for s in neg_review[:int(len(neg_review)*0.70)]:
    test_doc.append(s)


test_pos_review = test_doc[:len_pos_test]
test_neg_review = test_doc[len_pos_test:]

random.shuffle(test_doc)
test_c = test_doc[:int(len(test_doc)*0.75)]
prob_pos_review = (len(mega_pos_review))/(len(mega_doc))
prob_neg_review = (len(mega_neg_review))/(len(mega_doc))

acc_c_pos = 0
acc_c_neg = 0
test_prob_pos = 0
test_prob_pos = 0
for sent in test_c:
    test_prob_pos = prob_pos_review
    test_prob_neg = prob_neg_review
    for word in sent:
        if word in vocab:
            test_prob_pos = test_prob_pos*prob_pos_word.get(word)
            test_prob_neg = test_prob_neg*prob_neg_word.get(word)
    if test_prob_pos>test_prob_neg:
        acc_c_pos += 1
    if test_prob_neg>test_prob_pos:
        acc_c_neg += 1



print('Positive Reviews:',(acc_c_pos*100)/(len(test_pos_review)))


print('exec time = ', time.time()- start)
