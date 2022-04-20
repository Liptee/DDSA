import tools
from conf import k, MAX

class ChordNode:
    def __init__(self, id):
        self.id = id
        self.finger = {}
        self.start = {}
        for i in range(k):
            self.start[i] = (self.id+(2**i))%MAX
        self.predecessor = None
        self.succ = None

    def join(self, n1):
        if self == n1:
            for i in range(k):
                self.finger[i] = self
            self.predecessor = self
        else:
            self.init_finger_table(n1)
            self.update_others()

    def successor(self):
        self.succ = self.finger[0]
        return self.finger[0]

    def init_finger_table(self,n1):
        self.finger[0] = n1.find_successor(self.start[0])
        self.predecessor = self.successor().predecessor
        self.successor().predecessor = self
        self.predecessor.finger[0] = self
        for i in range(k-1):
            if tools.Ebetween(self.start[i+1],self.id,self.finger[i].id):
                self.finger[i+1] = self.finger[i]
            else :
                self.finger[i+1] = n1.find_successor(self.start[i+1])
    
    def find_successor(self, id):
        if tools.betweenE(id,self.predecessor.id,self.id):
            return self
        n = self.find_predecessor(id)
        return n.successor()

    def closest_preceding_finger(self,id):
        for i in range(k-1,-1,-1):
            if tools.between(self.finger[i].id,self.id,id):
                return self.finger[i]
        return self

    def update_others(self):
        for i in range(k):
            prev  = tools.decr(self.id,2**i)
            p = self.find_predecessor(prev)
            if prev == p.successor().id:
                p = p.successor()
            p.update_finger_table(self,i)
    
    def update_finger_table(self,s,i):
        if tools.Ebetween(s.id,self.id,self.finger[i].id) and self.id!=s.id:
            self.finger[i] = s
            p = self.predecessor
            p.update_finger_table(s,i)

    def find_predecessor(self,id):
        if id == self.id:
            return self.predecessor
        n1 = self
        while not tools.betweenE(id,n1.id,n1.successor().id):
            n1 = n1.closest_preceding_finger(id)
        return n1

    def update_others_leave(self):
        for i in range(k):
            prev  = tools.decr(self.id,2**i)
            p = self.find_predecessor(prev)
            p.update_finger_table(self.successor(),i)

    def leave(self):
        self.successor().predecessor = self.predecessor
        self.predecessor.setSuccessor(self.successor())
        self.update_others_leave()
        
    def setSuccessor(self,succ):
        self.finger[0] = succ

    def find_id(self, id):
        if self.id == id:
            return self.id
        for i in range(k):
            if self.finger[i].id == id:
                return self.finger[i]

        node = self.successor()
        for r in range(int(MAX/2)):
            if node.id == id:
                return node.id
            for i in range(k):
                if node.finger[i].id == id:
                    return node.finger[i]
            node = node.successor()

    def info(self):
        print(f'id: {self.id}')
        print(f'finger: {self.finger}')
        print(f'start: {self.start}')
        print(f'successor: {self.successor()}')
        print(f'predecessor: {self.predecessor}')