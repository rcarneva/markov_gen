class MarkovModel(object):
    def __init__(self, text_series, use_char=True, chars=5):
        self.markov = defaultdict(lambda: Counter())

        for text in text_series.ix[:]:
            lastword = [None] * chars
            ob = text if use_char else text.split()
            for c in ob:
                self.markov[tuple(lastword)][c] += 1
                lastword = lastword[1:] + [c]
            self.markov[tuple(lastword)][None] += 1

        self.chars = chars
        self.use_char = use_char
  
    def gen(self):
        lastword = [None] * self.chars
        gen = []

        while True:
            vals = self.markov[tuple(lastword)].values()
            tot = float(sum(vals))

            nextchar = np.random.choice(list(self.markov[tuple(lastword)].keys()), p=list(map(lambda v: v / tot, vals)))
            if nextchar is None:
                break
            gen += [nextchar]
            lastword = lastword[1:] + [nextchar]
        joiner = '' if self.use_char else ' '
        return joiner.join(gen)
