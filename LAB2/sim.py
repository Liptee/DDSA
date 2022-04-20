from ChordNode import ChordNode
from conf import MAX

joined = []
initiated = []

command = ""
while command != 'exit':
    command = input(':::')
    if command == f'init':
        id = input('unput id: ')
        exec(f'n{id} = ChordNode({id})')
        initiated.append(int(id))
    
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
            exec(f'n{i} = ChordNode({i})')
            initiated.append(i)
    
    if command == "join_all":
        for i in initiated:
            exec(f"n{i}.join(n{initiated[0]})")
            joined.append(f"{i} to {initiated[0]}")

    if command == "leave":
        id = input("id: ")
        exec(f'n{id}.leave()')

    if command == 'find_node':
        FROM = input('Choose your adress: ')
        target = int(input('Input finding id: '))
        if target in initiated:
            exec(f"print(n{FROM}.find_id({target}))")
        else: 
            print('Node was not found')
    
    if command == 'check_find':
        for id in initiated:
            print(f'for {id}')
            exec(f'print(n0.find_id({id}))')