import random
import os
import urllib.parse
from transitions.extensions import GraphMachine

default_prob = [0.01, 0.05, 0.08, 0.20, 0.60, 1.0]
s3_prob = [0.5, 1.0]
s4_prob = [0.2, 1.0]
s5_prob = [0.2, 1.0]
dirname = os.path.dirname(__file__)


class gotcha(object):
    def __init__(self, base):
        # The states argument defines the name of states
        states = ["ini", "default", "event", "star3", "star4", "star5", "state10"]
        # The trigger argument defines the name of the new triggering method
        transitions1 = [
            {"trigger": 'd', 'source': 'ini', 'dest': 'default'},
            {'trigger': 's3', 'source': 'ini', 'dest': 'star3'},
            {'trigger': 's4', 'source': 'ini', 'dest': 'star4'},
            {'trigger': 's5', 'source': 'ini', 'dest': 'star5'},
            {'trigger': 'eve', 'source': 'ini', 'dest': 'event'},
            {'trigger': 'to10', 'source': 'ini', 'dest': 'state10'},
            {'trigger': 'b', 'source': ["default", "event", "star3", "star4", "star5", "state10"], 'dest': 'ini'}]
        self.machine = GraphMachine(model=self, states=states, transitions=transitions1, initial="ini")

        states2 = ["africa", "normal", "europe"]
        transitions2 = [
            {"trigger": 'n_to_e', 'source': 'normal', 'dest': 'europe'},
            {"trigger": 'e_to_n', 'source': 'europe', 'dest': 'normal'},
            {"trigger": 'n_to_a', 'source': 'normal', 'dest': 'africa'},
            {"trigger": 'a_to_n', 'source': 'africa', 'dest': 'normal'}
        ]
        self.submachine = GraphMachine(states=states2, transitions=transitions2, initial="normal")

        self.get_graph().draw("fsm1.png", prog="dot")
        self.submachine.get_graph().draw("fsm2.png", prog="dot")
        self.base = base
        self.total = 0
        self.total3 = 0
        self.total4 = 0
        self.total5 = 0
        pass

    def test(self):
        t = self.total
        s3r = self.total3/t
        s4r = self.total4/t
        s5r = self.total5/t
        print('from '+self.submachine.state, end=" ")
        if 0.7 < s3r < 0.85:
            if self.submachine.state == 'europe':
                self.submachine.e_to_n()
                pass
            elif self.submachine.state == 'africa':
                self.submachine.a_to_n()
                pass
            pass
        elif s3r <= 0.7 or s5r >= 0.07 or s4r >= 0.18:
            if self.submachine.state == 'normal':
                self.submachine.n_to_e()
                pass
            elif self.submachine.state == 'africa':
                self.submachine.a_to_n()
                self.submachine.n_to_e()
                pass
            pass
        else:
            if self.submachine.state == 'normal':
                self.submachine.n_to_a()
                pass
            elif self.submachine.state == 'europe':
                self.submachine.e_to_n()
                self.submachine.n_to_a()
                pass
            pass
        print('to ' + self.submachine.state)
        pass

    def show(self):
        if self.total == 0:
            return "total: 0"
        else:
            return "total: " + str(self.total) + "\n5★=" + str(self.total5 / self.total*100) + "%" + "\n4★=" + \
                   str(self.total4 / self.total*100) + "%" + "\n3★=" + str(self.total3 / self.total*100) + "%"
        pass

    def enterdefault(self):
        self.d()
        print(self.state)
        self.b()
        print(self.state)
        return self.pick()
        pass

    def pick(self):
        p = random.random()
        r = "in default mode\nyou get "
        t = False
        l = self.base
        if p < default_prob[0]:
            r += "5★ servant "
            n = random.choice(os.listdir("img/star5"))
            r += n.strip(".png")
            l += "img/star5/" + urllib.parse.quote(n)
            self.total5 += 1
            pass
        elif p < default_prob[1]:
            r += "5★ craft "
            n = random.choice(os.listdir("craft/star5"))
            r += n.strip(".png")
            l += "craft/star5/" + urllib.parse.quote(n)
            self.total5 += 1
            pass
        elif p < default_prob[2]:
            r += "4★ servant "
            n = random.choice(os.listdir("img/star4"))
            r += n.strip(".png")
            l += "img/star4/" + urllib.parse.quote(n)
            self.total4 += 1
            pass
        elif p < default_prob[3]:
            r += "4★ craft "
            n = random.choice(os.listdir("craft/star4"))
            r += n.strip(".png")
            l += "craft/star4/" + urllib.parse.quote(n)
            self.total4 += 1
            pass
        elif p < default_prob[4]:
            r += "3★ servant "
            n = random.choice(os.listdir("img/star3"))
            r += n.strip(".png")
            l += "img/star3/" + urllib.parse.quote(n)
            self.total3 += 1
            t = True
            pass
        elif p < default_prob[5]:
            r += "3★ craft "
            n = random.choice(os.listdir("craft/star3"))
            r += n.strip(".png")
            l += "craft/star3/" + urllib.parse.quote(n)
            self.total3 += 1
            t = True
            pass
        self.total += 1
        self.test()
        return l, r, t
        pass

    def pick10(self):
        self.to10()
        print(self.state)
        t = True  # need replace
        res = []
        for i in range(0, 10):
            r = self.pick()
            t &= r[2]
            res.append(r)
            pass
        if t == True:
            print("need replace")
            index = int(random.random()*10)
            r = "in default mode\nyou get "
            l = self.base
            r += "4★ craft "
            n = random.choice(os.listdir("craft/star4"))
            r += n.strip(".png")
            l += "craft/star4/" + urllib.parse.quote(n)
            self.total4 += 1
            self.total3 -= 1
            res[index] = l, r, False
            pass
        else:
            print("no need replace")
            pass
        self.b()
        print(self.state)
        return res
        pass

    def enters3(self):
        self.s3()
        print(self.state)
        r = "in 3★ mode\nyou get "
        l = self.base
        p = random.random()
        if p < s3_prob[0]:
            r += "servant "
            n: str = random.choice(os.listdir("img/star3"))
            r += n.strip(".png")
            l += "img/star3/" + urllib.parse.quote(n)
        else:
            r += "craft "
            n: str = random.choice(os.listdir("craft/star3"))
            r += n.strip(".png")
            l += "craft/star3/" + urllib.parse.quote(n)
        self.b()
        print(self.state)
        self.test()
        return l, r
        pass

    def enters4(self):
        self.s4()
        print(self.state)
        r = "in 4★ mode\nyou get "
        l = self.base
        p = random.random()
        if p < s4_prob[0]:
            r += "servant "
            n: str = random.choice(os.listdir("img/star4"))
            r += n.strip(".png")
            l += "img/star4/" + urllib.parse.quote(n)
        else:
            r += "craft "
            n: str = random.choice(os.listdir("craft/star4"))
            r += n.strip(".png")
            l += "craft/star4/" + urllib.parse.quote(n)
        self.b()
        print(self.state)
        self.test()
        return l, r
        pass

    def enters5(self):
        self.s5()
        print(self.state)
        r = "in 5★ mode\nyou get "
        l = self.base
        p = random.random()
        if p < s5_prob[0]:
            r += "servant "
            n: str = random.choice(os.listdir("img/star5"))
            r += n.strip(".png")
            l += "img/star5/" + urllib.parse.quote(n)
        else:
            r += "craft "
            n: str = random.choice(os.listdir("craft/star5"))
            r += n.strip(".png")
            l += "craft/star5/" + urllib.parse.quote(n)
        self.b()
        print(self.state)
        self.test()
        return l, r
        pass

    def enterevent(self):
        self.eve()
        print(self.state)
        r = "in event mode\nyou get "
        l = self.base
        r += "event servant "
        n: str = random.choice(os.listdir("img/event"))
        r += n.strip(".jpg")
        l += "img/event/" + urllib.parse.quote(n)
        self.b()
        print(self.state)
        return l, r
        pass
    pass


if __name__ == '__main__':
    g = gotcha("")
    for i in range(0, 10):
        print(g.pick10())
