import random

k = 10
MAX = 2**k


def decr(value,size):
    if size <= value:
        return value - size
    else:
        return MAX-(size-value)
        
def between(value,init,end):
    if init == end:
        return True
    elif init > end :
        shift = MAX - init
        init = 0
        end = (end +shift)%MAX
        value = (value + shift)%MAX
    return init < value < end

def Ebetween(value,init,end):
    if value == init:
        return True
    else:
        return between(value,init,end)

def betweenE(value,init,end):
    if value == end:
        return True
    else:
        return between(value,init,end)

class Node:
    def __init__(self,id):
        self.id = id
        self.finger = {}
        self.start = {}
        for i in range(k):
            self.start[i] = (self.id+(2**i)) % (2**k)
        self.predecessor = None

    def successor(self):
        return self.finger[0]
    
    def find_successor(self,id):  
        print(f"FIND_SUC: начинаю работу с входными данными {self.id} узел и {id}")
        print(f'FIND_SUC: начинаю проверку betweenE для {id} в пределах {self.predecessor.id} и {self.id}')
        if betweenE(id,self.predecessor.id,self.id):
            print('FIND_SUC: проверка прошла успешно')
            print(f"FIND_SUC: возвращаю {self.id} узел и заканчиваю работу")
            return self
        print("FIND_SUC: проверка не прошла")
        print(f'FIND_SUC: высчитываю n. Запускаю для этого функцию find_predecessor. И передаю в нее значения {self.id} узел как self, и {id} как id')
        n = self.find_predecessor(id)
        print(f'FIND_SUC: n равен {n}')
        print(f"FIND_SUC: возвращаю {n.successor().id} узел и заканчиваю работу")
        return n.successor()
    
    def find_predecessor(self,id):
        print(f'FIND_PRED: говорит функция find_predecessor. Начинаю работу с входными данными {self.id} узел и {id}')
        print(f'FIND_PRED: Проверяю равенство входных данных')
        if id == self.id:
            print(f"FIND_PRED: проверка прошла успешно. Возвращаю {self.predecessor.id} узел")
            print('FIND_PRED: заканчиваю работу')
            return self.predecessor
        print(f"FIND_PRED: проверка не прошла. Инициализирую значение n1 равное узлу {self.id}")
        n1 = self
        print(f"FIND_PRED: начинаю цикл пока not_betweenE для id={id} в пределах {n1.id} и {n1.successor().id} справедливо")
        while not betweenE(id,n1.id,n1.successor().id):
            print(f"FIND_PRED: для подсчета n1 обращаюсь к функции closest_preceding_finger. Передаю в нее значения {n1.id} узел как self и {id} как id")
            n1 = n1.closest_preceding_finger(id)
            print(f'FIND_PRED: перезаписал значение n1, как {n1}')
        print(f"FIND_PRED: цикл прерван. Возращаю узел {n1.id} и заканчиваю работу")
        return n1
    
    def closest_preceding_finger(self,id):
        print(f'CPF: говорит функция closest_preceding_finger с входными значениями узел {self.id} и {id}')
        print(f'CPF: начинаю цикл для i in range({k-1},-1,-1)')
        for i in range(k-1,-1,-1):
            print(f'CPF: начинаю проверку between для self.finger[{i}].id в пределах {self.id} и {id}')
            if between(self.finger[i].id,self.id,id):
                print(f"CPF: проверка прошла успешно. Возвращаю {self.finger[i].id} узел и заканичваю работу")
                return self.finger[i]
        print(f'CPF: цикл закончен, но никто не смог пройти проверку. Поэтому возвращаю {self.id} узел')
        return self
        
    
    def join(self,n1):
        print("Началась функция join")
        print(f'JOIN: self = {self.id} узел, n1 = {n1.id} узел')
        if self == n1:
            print(f'JOIN: начался цикл for для i in range{k}')
            for i in range(k):
                self.finger[i] = self
                print(f'JOIN: self.finger[{i}] = {self.finger[i].id} узел')
                print(f'JOIN: я изменил список finger для {self.id} узла. Теперь: {self.finger}')
            self.predecessor = self
            print(f'JOIN: Я нашел предшественника {self.id} узел для {self.id} узла')
        else:
            print(f"JOIN: запускаю функию init_finger_table. Передаю в нее значения {self.id} узел, как self и {n1.id} узел как n1")
            self.init_finger_table(n1)
            print(f'JOIN: запускаю функцию update_others. Передаю в нее значение {self.id} узел как self')
            self.update_others()  
        print('JOIN: я закончил свою работу')
        print()
        print()

    def init_finger_table(self,n1):
        print('Началась функцию init_finger_table')
        print(f'IFT: Начаю свою работу. Входные значения self = {self.id} узел, n1 = {n1.id} узел')
        print(f'IFT: запускаю функцию find_successor. Передаю значения {n1.id} узел, как self и {self.start[0]} как id')
        self.finger[0] = n1.find_successor(self.start[0])
        print(f'IFT: я добавил self.finger[0] для {self.id} узла. Он равен {self.finger[0].id} узлу')
        self.predecessor = self.successor().predecessor
        print(f'IFT: Я нашел предшественника для {self.id} узла. Теперь он {self.predecessor.id} узел')
        print(f'IFT: перезаписываю предшественника для {self.successor().id} узла. Теперь его предшественник {self.id} узел')
        self.successor().predecessor = self
        self.predecessor.finger[0] = self
        print(f"IFT: изменил finger[0] для {self.predecessor.id} узла. Теперь он равен {self.id} узлу")
        print(f'IFT: начинаю цикл для i in range({k-1})')
        for i in range(k-1):
            if Ebetween(self.start[i+1],self.id,self.finger[i].id):
                self.finger[i+1] = self.finger[i]
                print(f'IFT: так как {self.start[i+1]} лежит от включая {self.id} до не включая {self.finger[i].id}')
                print(f'IFT: то self.finger[{i+1}] = {self.finger[i+1].id} узел')
            else :
                print(f'IFT: так как {self.start[i+1]} не принадлежит от включая {self.id} до не включая {self.finger[i].id}')
                print(f'IFT: запускаю функцию find_successor. Передаю в нее значения {n1} как self, и {self.start[i+1]} как id')
                self.finger[i+1] = n1.find_successor(self.start[i+1])
                print(f'IFT: self.finger[{i+1}] после функции find_successor равен {self.finger[i+1]}')
        print('IFT: я закончил свою работу')

    def update_others(self):
        print('UPOT: говорит функция update_otheres. Начинаю свою работу.')
        print('UPOT: начинаю цикл для i in range({k})')
        for i in range(k):
            print(f'UPOT: обращаюсь в внешней функции decr для подсчета prev. Передаю в нее значения {self.id} и {2**i}')
            prev  = decr(self.id,2**i)
            print(f"UPOT: prev равен {prev}")
            print(f'UPOT: для подсчета p запускаю функцию find_predecessor. Передаю ему значения {self.id} узла как self, и prev, то есть {prev} как id')
            p = self.find_predecessor(prev)
            print(f'UPOT: find_predecessor закончил подсчет p. p равен {p.id} узлу')
            print(f'UPOT: запускаю проверку для prev, равен ли он p.successor().id, то есть {p.successor().id}')
            if prev == p.successor().id:
                print('UPOT: проверка прошла успешно')
                print(f'UPOT: перезаписываю {p.id} как своего наследника')
                p = p.successor()
            print(f'UPOT: проверка не прошла. Запускаю функцию update_finger_table. Передаю в нее значения {p.id} узел как self, {self.id} узел как s, и {i} как i.')
            p.update_finger_table(self,i)
        print('UPOT: заканчиваю свою работу')


    def update_finger_table(self,s,i):
        print(f'UFT: говорит функция update_finger_table с входными данными узел {self.id}, узел {s.id} и {i}')
        print(f'UFT: начинаю проверку Ebetween для s.id в пределах {self.id} и {self.finger[i].id}')
        if Ebetween(s.id,self.id,self.finger[i].id) and self.id!=s.id:
            self.finger[i] = s
            print(f'UFT: перезаписываю self.finger[{i}] на входное значение {s.id} узел')
            p = self.predecessor
            print(f'UFT: запускаю другую функцию UFT с входными параметрами узел {p.id}, узел {s.id} и {i}')
            p.update_finger_table(s,i)
            print(f'UFT: finger_table обновлен')
        print(f"UFT: проверка не прошла. Завершаю свою работу.")

    def update_others_leave(self):
        print(f'UOL: говорит функция update_others_leave. Начинаю обновление для исключение узла {self.id} из ситемы')
        print(f"UOL: запускаю цикл для i in range({k})")
        for i in range(k):
            print(f"UOL: для подсчета prev обращаюсь к внешней функции decr с параметрами {self.id} и {2**i}")
            prev  = decr(self.id,2**i)
            print(f"UOL: prev равен {prev}")
            print(f"UOL: для нахождения p запускаю функцию find_predecessor с параметрами узла {self.id} как self и prev={prev} как id")
            p = self.find_predecessor(prev)
            print(f'UOL: начинаю обновлять таблицу для p_Узла={p.id} с помощью функции update_finger_table. Передаю значения узла {p.id}, узла {self.successor().id}  и {i}')
            p.update_finger_table(self.successor(),i)
        print('UOL: цикл окончен и я закончил свою работу')

    def leave(self):
        print(f'LEAVE: начинаю исключать узел {self.id} из системы')
        self.successor().predecessor = self.predecessor
        print(f"LEAVE: изменила предшественника для наследника, на предшественника узла {self.id}")
        self.predecessor.setSuccessor(self.successor())
        print(f'LEAVE: изменила наследника для предшественника на наследника узла {self.id}')
        print(f'LEAVE: запускаю функцию update_others_leave с параметром {self.id} узла')
        self.update_others_leave()
        print('LEAVE: я закончил свою работу')
        print()
        print()
        
    def setSuccessor(self,succ):
        self.finger[0] = succ

    def info(self):
        print(f'id: {self.id}')
        print(f'finger: {self.finger}')
        print(f'start: {self.start}')
        print(f'predeccessor: {self.predecessor}')
        print()


joined = []
initiated = []

command = ""
while command != 'exit':
    command = input(':::')
    if command == f'init':
        id = input('unput id: ')
        exec(f'n{id} = Node({id})')
        initiated.append(id)
    
    if command == 'join':
        FROM = input("id: ")
        TO = input("where id: ")
        exec(f'n{FROM}.join(n{TO})')
        joined.append(f'{FROM} to {TO}')

    if command == 'info':
        id = input("id: ")
        exec(f'n{id}.info()')

    if command == "list_init":
        print(initiated)

    if command == "list_join":
        print(joined)

    if command == "init_max":
        for i in range(MAX):
            exec(f'n{i} = Node({i})')
            initiated.append(i)
    
    if command == "join_all":
        for i in initiated:
            exec(f"n{i}.join(n{initiated[0]})")
            joined.append(f"{i} to {initiated[0]}")

    if command == "leave":
        id = input("id: ")
        exec(f'n{id}.leave()')
