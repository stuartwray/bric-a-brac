#!/usr/bin/python3

import math
import random
import itertools
import collections

# helper routines

def log2(x):
    return math.log(x, 2)

def Entropy(counts):
    total = sum(counts)

    # Cope with tricky case ...
    if total == 0:
        return 0

    # entropy, H = Sum (Pi * log2 (1/Pi))  
    probs = (i/total for i in counts if i != 0)
    return sum(p * log2(1/p) for p in probs)

#-----------------------------------------------------

class Colour:
    def __init__(self, colour):
        self.colour = colour

    def __str__(self):
        return self.colour

    __repr__ = __str__

    def __eq__(self, other):
        return self.colour == other.colour

    def __ne__(self, other):
        return not(self == other)

    def __hash__(self):
        return hash(self.colour)

# This would be faster if we just declared all_colours as a tuple of strings:
# all_colours = ("red", "green", etc ...
# But this makes it more like the C++ version:

all_colours = (Colour("red"), 
               Colour("green"),
               Colour("blue"),
               Colour("yellow"), 
               Colour("white"), 
               Colour("black"))
    
class Position:
    WIDTH = 4
    
    def __init__(self, *pegs):
        self.pegs = tuple(pegs)
        count_map = collections.defaultdict(int)
        for peg in self.pegs:
            count_map[peg] += 1
        # for this to work, all_colours must not change
        self.counts = [count_map[p] for p in all_colours]
    
    def __str__(self):
        return ".".join(str(p) for p in self.pegs)

    __repr__ = __str__

    def __eq__(self, other):
        return all(s == o for s, o in zip (self.pegs, other.pegs))
        
    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(self.pegs)

    def Mark(self, correct):
        # do black marks
        pairs = zip(self.pegs, correct.pegs)
        blacks = sum([1 for s, c in pairs if s == c]) ##

        # do total (black+white) marks
        pairs = zip(self.counts, correct.counts)
        total = sum([min(s, c) for s, c in pairs])

        # combined marks 
        return "b" * blacks + "w" * (total - blacks)

    @classmethod
    def MakeRandomPosition(cls, colours):
        pegs = [random.choice(colours) for _ in range(cls.WIDTH)]
        return cls(*pegs)

    @classmethod
    def MakeAllPositions(cls, colours):
        return list(cls(*pegs) for pegs in \
                    itertools.product(colours, repeat=cls.WIDTH))
    
#-----------------------------------------------------

# This is the secret position to guess
secret = Position.MakeRandomPosition(all_colours);
print("Secret is", secret)

# This is the list of challenges that we haven't used yet
challenges = Position.MakeAllPositions(all_colours);

# This is the list of positions that are still plausible,
# given the responses to challenges so far
candidates = Position.MakeAllPositions(all_colours);

attempt = 1;

while (True):
    print("(%d) Candiates left = %d" % (attempt, len(candidates)))
    attempt += 1

    if len(candidates) == 1:
        # We have notionally finished, but we still have to say what the
        # answer is
        guess = candidates[0]
    else:
        # Find the challenge with the highest entropy
        max_ent = -1.0;
      
        # For all remaining challenges ...
      
        for challenge in challenges:
            # Mark every remaining candidate
            mark2Count = collections.defaultdict(int)
            for candidate in candidates:
                mark2Count[candidate.Mark(challenge)] += 1
        
            # Determine the entropy associated with this distribution of marks

            entropy = Entropy(mark2Count.values())
            
            # is this the best so far?
            
            if (entropy > max_ent):
                max_ent_pos = challenge
                max_ent = entropy;

        guess = max_ent_pos
        print("    Max entropy ", max_ent)

    # Remove the challenge we just used
    challenges.remove(guess)
    print("    Guess is ", guess)

    # ---------------------------------------------------
    # This part is notionally done by the other player

    mark = secret.Mark(guess)
    print('Mark is "%s"' % mark)

    if (mark == "b" * Position.WIDTH):
        answer = guess;
        break

    # Now back to the guesser
    # ---------------------------------------------------

    # Remove the candidates that are inconsistent with the answer we got

    candidates = [c for c in candidates if c.Mark(guess) == mark]

print("Solution is ", answer)
print("------------------------------------------------------")


    

