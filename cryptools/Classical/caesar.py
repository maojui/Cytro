import re
from pycipher import Caesar
      
def break_caesar(ctext):
    """
    This function will break the Caesar Cipher with english frequence detect,
    therefore, this will not do well on short cipher QwQ.
    """
    from ngram_score import ngram_score
    fitness = ngram_score('./English_Frequency/quadgram.pickle') # load our quadgram statistics
    # make sure ciphertext has all spacing/punc removed and is uppercase
    ctext = re.sub('[^A-Z]','',ctext.upper())
    # try all possible keys, return the one with the highest fitness
    scores = []
    for i in range(26):
        scores.append((fitness.score(Caesar(i).decipher(ctext)),i))
    print('best candidate with key (a,b) = {}:'.format(str(max_key[1])))
    print(Caesar(max_key[1]).decipher(ctext))
    return max(scores)

def brute(ctext):
    """
    Show all possible 26 character decipher.
    """
    # make sure ciphertext has all spacing/punc removed and is uppercase
    ctext = re.sub('[^A-Z]','',ctext.upper())
    ptxt = []
    for i in range(26):
        ptxt.append(Caesar(i).decipher(ctext))
        print('{i:02} : {}'.format(i,ptxt[i]))
    return ptxt
    
