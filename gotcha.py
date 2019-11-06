import random
import os

default_prob = [0.05, 0.20, 1.0]
dirname = os.path.dirname(__file__)

class gotcha:
    def __init__(self, base):
        self.base = base
        pass

    def enterdefault(self):
        p = random.random()
        r = "in default mode\nyou get "
        l = self.base
        if p < default_prob[0]:
            r += "5★ "
            n = random.choice(os.listdir("img/star5"))
            r += n
            l += "img/star5/"+n
            pass
        elif p < default_prob[1]:
            r += "4★ "
            n = random.choice(os.listdir("img/star4"))
            r += n
            l += "img/star4/" + n
            pass
        elif p < default_prob[2]:
            r += "3★ "
            n = random.choice(os.listdir("img/star3"))
            r += n
            l += "img/star3/" + n
            pass
        return l, r
        pass

    def enters0(self):
        pass

    def enters1(self):
        pass

    def enters2(self):
        pass

    def enters3(self):
        pass

    def enters4(self):
        pass

    def enters5(self):
        pass

    def enterevent(self):
        r = "in event mode\nyou get "
        l = self.base
        r += "event servant "
        n = random.choice(os.listdir("img/event"))
        r += n
        l += "img/event/" + n
        return l.replace(" ","%20"), r
        pass

    pass
"""
g = gotcha("https://joejoe2.github.io/LineBot/")
print(g.enterdefault())
print(g.enterevent()[0])"""
