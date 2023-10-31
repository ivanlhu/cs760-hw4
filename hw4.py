#!/usr/bin/env python3

import math

def lettercount(filename):
    count = [0] * 27
    with open(filename) as file:
        for line in file:
            for ch in line:
                if ord(ch) >= ord('a') and ord(ch) <= ord('z'):
                    count[ord(ch)-ord('a')] += 1
                elif ch == ' ':
                    count[26] += 1
    return count

def priors():
    raw_totals = {'e': 0, 'j': 0, 's': 0}
    for t in range(10):
        for lang in ['e', 'j', 's']:
            raw_totals[lang] += sum(lettercount('languageID/'+lang+str(t)+'.txt'))
    total = raw_totals['e']+raw_totals['j']+raw_totals['s']
    priors = {}
    for lang in ['e', 'j', 's']:
        priors[lang] = math.log10((raw_totals[lang]+0.5)/(total+3*0.5))
    return priors

def letterprobs():
    counts = [0] * 27
    for t in range(10):
        for lang in ['e', 'j', 's']:
            count = lettercount('languageID/'+lang+str(t)+'.txt')
            for i in range(27):
                counts[i] += count[i]
    total = sum(counts)
    probs = [math.log10((counts[i]+0.5)/(total+27*0.5)) for i in range(27)]
    return probs
    

def class_cond_probs(lang):
    counts = [0] * 27
    for t in range(10):
        count = lettercount('languageID/'+lang+str(t)+'.txt')
        for i in range(27):
            counts[i] += count[i]
    total = sum(counts)
    probs = [0] * 27
    for i in range(27):
        probs[i] = math.log10((counts[i]+0.5)/(total+27*0.5))
    return probs

def estimate_prob(lettercount, probs):
    p = 0.0
    for i in range(27):
        p += lettercount[i] * probs[i]
    return p

def pow10str(x):
    e = math.floor(x)
    b = math.pow(10,x-e)
    return '{:6f}e{:d}'.format(b,e)

def p1():
    pr = priors()
    print("English: "+str(math.pow(10,pr['e'])))
    print("Japanese: "+str(math.pow(10,pr['j'])))
    print("Spanish: "+str(math.pow(10,pr['s'])))
    print(' ')

def p2_3():
    english = class_cond_probs('e')
    japanese = class_cond_probs('j')
    spanish = class_cond_probs('s')
    print("English letter probabilities:")
    for i in range(26):
        print("  "+chr(i+ord('a'))+": "+pow10str(english[i]))
    print("spc: "+pow10str(english[i]))
    print(" ")

    print("Japanese letter probabilities:")
    for i in range(26):
        print("  "+chr(i+ord('a'))+": "+pow10str(japanese[i]))
    print("spc: "+pow10str(japanese[i]))
    print(" ")

    print("Spanish letter probabilities:")
    for i in range(26):
        print("  "+chr(i+ord('a'))+": "+pow10str(spanish[i]))
    print("spc: "+pow10str(spanish[i]))
    print(" ")

def p4():
    print("e10.txt bag of words:")
    print(lettercount('languageID/e10.txt'))

def p5():
    e = class_cond_probs('e')
    j = class_cond_probs('j')
    s = class_cond_probs('s')
    prior = priors()
    letters = letterprobs()
    x = lettercount('languageID/e10.txt')
    base = sum([ x[i]*letters[i] for i in range(27)])  
    eprob = estimate_prob(x, e)
    jprob = estimate_prob(x, j)
    sprob = estimate_prob(x, s)
    print("Probability of x given lang='e':")
    print(pow10str(eprob))
    print("Probability of x given lang='j':")
    print(pow10str(jprob))
    print("Probability of x given lang='s':")
    print(pow10str(sprob))

    print("Probability of 'e' given x")
    print(pow10str(eprob+prior['e']-base))
    print("Probability of 'j' given x")
    print(pow10str(jprob+prior['j']-base))
    print("Probability of 's' given x")
    print(pow10str(sprob+prior['s']-base))

def p6lang(lang):
    e = class_cond_probs('e')
    j = class_cond_probs('j')
    s = class_cond_probs('s')
    prior = priors()
    letters = letterprobs()

    xs = [ lettercount('languageID/'+lang+str(i)+'.txt') for i in range(10,20)]
    predictions = {'e': 0, 'j': 0, 's': 0}
    for x in xs:        
        base = sum([ x[i]*letters[i] for i in range(27)])     
        eprob = estimate_prob(x, e)+prior['e']-base
        jprob = estimate_prob(x, j)+prior['j']-base
        sprob = estimate_prob(x, s)+prior['s']-base
        if eprob > jprob and eprob > sprob:
            predictions['e'] += 1
        elif jprob > sprob:
            predictions['j'] += 1
        else:
            predictions['s'] += 1
    return predictions
        
def p6():
    print("Actual English:")
    print(p6lang('e'))
    print("Actual Japanese:")
    print(p6lang('j'))
    print("Actual Spanish:")
    print(p6lang('s'))
    

p5()
