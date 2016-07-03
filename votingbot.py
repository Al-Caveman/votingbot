# totally badass voting script by freenode's caveman that, unlike others,
# actually does some statistical significance testing.
#
# licensed under MIT license
#
# before you use this code, please say that i wrote it and put my email there
# and mention that i am in freenode's #gentoo-chat-exile, and ##politics. also
# point out this url: http://github.com/al-caveman -- i really love internet
# points.
#
# contact me <toraboracaveman@gmaiol.com>

import operator
import random
import sys

#
# danger zone begin
#
# two handy functions. these could be too advanced for you, but feel free to
# ask me for help. please don't feel too bad about yourself. it's okay for you
# to not understand this.
def gap(options_rank):
    return options_rank[0][1] - options_rank[1][1]

def simrandvote(N_options, N_votes):
    lol = [random.random() for i in range(0, N_options)]
    rofl = sum(lol)
    lmfao = [l/rofl for l in lol]
    d = {}
    for i in range(0, N_options):
        d[i] = int(lmfao[i] * N_votes + 0.5)
    return d
#
# danger zone end
#


# ballot
d = {}
d['yes'] = 5
d['no'] = 1
d['dunno'] = 2

# so we got 3 options
N_options = len(d)

# and we have 8 voters
N_votes = sum([d[k] for k in d])

# settings
R = 100000
random.seed(0)

# rank options by their votes
options_rank = sorted(d.items(), key=operator.itemgetter(1), reverse=True)

# how extreme is the lead of the first winning option against the 2nd winning
# option?
winning_gap = gap(options_rank)

# compute p value
sys.stderr.write('simulating')
p = 0
for r in range(0, R):
    # simulate a noisy random vote
    d_random = simrandvote(N_options, N_votes)

    # find the winning gap of this random vote
    options_rank_random = sorted(d_random.items(),
                                 key=operator.itemgetter(1),
                                 reverse=True)
    winning_gap_random = gap(options_rank_random)

    # ar business
    if winning_gap_random >= winning_gap:
        p += 1
        if (r % (R/1000)) == 0:
            sys.stderr.write('+')
    else:
        if (r % (R/1000)) == 0:
            sys.stderr.write('-')
    sys.stderr.flush()
sys.stderr.write(' ok\n')

print('p value is: %f' % (float(p+1)/float(R+1)))

