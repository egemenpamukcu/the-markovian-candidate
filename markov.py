'''
Doc: markov.py
Markov models for speaker recognition

'''

import sys
import math
import hash_table

HASH_CELLS = 57


class Markov:

    def __init__(self, k, s):
        '''
        Construct a new k-order Markov model using the statistics of string "s"
        '''
        self.k = k
        self.s = s
        self.txt = self.s[-self.k:] + self.s
        self.alphabet = len(set(s))
        self.d = hash_table.Hashtable(HASH_CELLS, hash_table.Hashtable(self.alphabet, 0))
        for i, l in enumerate(self.s):
            self.d[self.txt[i : i + self.k]] = self.d[self.txt[i : i + self.k]]
            self.d[self.txt[i : i + self.k]][l] += 1


    def log_probability(self, s):
        '''
        Get the log probability of string "s", given the statistics of
        character sequences modeled by this particular Markov model
        This probability is *not* normalized by the length of the string.
        '''
        self.log_prob = 0
        self.new_s = s
        self.new_txt = self.new_s[-self.k:] + self.new_s
        for i, l in enumerate(self.new_s):
            count = self.d[self.new_txt[i : i + self.k]][l]
            tot = sum(self.d[self.new_txt[i : i + self.k]].values())
            prob = (count + 1) / (self.alphabet + tot)
            self.log_prob += math.log(prob)
        return self.log_prob

def identify_speaker(speaker_a, speaker_b, unknown_speech, k):
    '''
    Given sample text from two speakers, and text from an unidentified speaker,
    return a tuple with the *normalized* log probabilities of each of the
    speakers uttering that text under a "k" order character-based Markov model,
    and a conclusion of which speaker uttered the unidentified text
    based on the two probabilities.
    '''
    model_a = Markov(k, speaker_a)
    model_b = Markov(k, speaker_b)
    prob_a = model_a.log_probability(unknown_speech) / len(unknown_speech)
    prob_b = model_b.log_probability(unknown_speech) / len(unknown_speech)
    conc = 'B'
    if prob_a > prob_b:
        conc = 'A'
    return(prob_a, prob_b, conc)