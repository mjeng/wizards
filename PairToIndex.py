class PairToIndex:

    base = 10

    def __init__(self, w1, w2, base):
        """
        Assuming w1 < w2 is our constraint
        """
        self.rep_num = self.convert_from_pair(w1, w2)
        self.w1, self.w2 = w1, w2
        self.base = base

    @classmethod
    def convert_to_pair(self, num):
        """
        Assumes 2 digits needed
        """
        w1 = 1 + num // cls.base
        w2 = 1 + num % cls.base
        return w1, w2

    @classmethod
    def convert_from_pair(cls, d1, d2):
        return cls.base * (d1 - 1) + (d2 - 1)
        #return d1 + cls.base * d2

    def __repr__(self):
        # return ""
        return "w" + str(self.w1) + " < w" + str(self.w2)
