import os
import random
import urllib.parse

from transitions.extensions import GraphMachine

default_prob = [0.05, 0.20, 1.0]
dirname = os.path.dirname(__file__)


class gotcha(GraphMachine):
    def __init__(self, base):
        self.machine = GraphMachine(model=self,
                                    states=["ini", "default", "s0", "s1", "s2", "s3", "s4", "s5", "event"],
                                    transitions=[
                                        {
                                            "trigger": "enter",
                                            "source": "ini",
                                            "dest": "default",
                                            "conditions": "is_going_to_default"
                                        },
                                        {"trigger": "go_back", "source": ["default", "s0", "s1", "s2", "s3", "s4", "s5", "event"], "dest": "ini"},
                                    ],
                                    initial="default",
                                    auto_transitions=False,
                                    show_conditions=True,
                                    )
        self.base = base
        self.total = 0
        self.total3 = 0
        self.total4 = 0
        self.total5 = 0
        pass

    def show(self):
        if self.total == 0:
            return "total: 0"
        else:
            return "total: " + str(self.total) + "  5★=" + str(self.total5 / self.total) + "%" + "  4★=" + \
                   str(self.total4 / self.total) + "%" + "  3★=" + str(self.total3 / self.total) + "%"
        pass

    def is_going_to_default(self):
        return True
        pass

    def on_enter_default(self):
        p = random.random()
        r = "in default mode\nyou get "
        l = self.base
        if p < default_prob[0]:
            r += "5★ "
            n = random.choice(os.listdir("img/star5"))
            r += n.strip(".png")
            l += "img/star5/" + urllib.parse.quote(n)
            self.total5 += 1
            pass
        elif p < default_prob[1]:
            r += "4★ "
            n = random.choice(os.listdir("img/star4"))
            r += n.strip(".png")
            l += "img/star4/" + urllib.parse.quote(n)
            self.total4 += 1
            pass
        elif p < default_prob[2]:
            r += "3★ "
            n = random.choice(os.listdir("img/star3"))
            r += n.strip(".png")
            l += "img/star3/" + urllib.parse.quote(n)
            self.total3 += 1
            pass
        self.total += 1
        self.go_back()
        return l, r
        pass

    def on_exit_default(self):
        print("exe default")

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
        n: str = random.choice(os.listdir("img/event"))
        r += n.strip(".jpg")
        l += "img/event/" + urllib.parse.quote(n)
        return l, r
        pass

    pass
