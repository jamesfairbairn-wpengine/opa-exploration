import json
from random import randint, choice, sample
from collections import namedtuple
from models import Role, Binding, DataObject
import argparse

names = ['alice', 'bob', 'frank', 'neil', 'shane', 'rachel', 'james', 'phil', 'chris', 'daithi', 'reginald', 'oprah', 'obama', 'trump', 'brian', 'charles', 'nathan']
last_names = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson']

object_names = ['widget', 'app', 'website', 'computer', 'server', 'database', 'tree', 'chocolate', 'cheese', 'monitor', 'hand', 'foot']

object_operations = ['read', 'write', 'own']

def create_random_user():
    return f'{choice(names)} {choice(last_names)} {randint(0, 1000000)}'

def create_random_role():
    operation = choice(object_operations)
    resource = choice(object_names)
    name = f'{resource}-{operation}{"r" if operation.endswith("e") else "er"}-{randint(0, 1000000)}'
    return Role(operation, resource, name)

def main(role_size, users_size, bindings_size):
    users = set()
    roles = set()
    bindings = set()

    while len(users) < users_size:
        users.add(create_random_user())

    while len(roles) < role_size:
        roles.add(create_random_role())

    while len(bindings) < bindings_size:
        binding = Binding(sample(users, 1)[0], sample(roles, 1)[0].name)
        bindings.add(binding)

    with open('users.json', 'w') as uf:
        json.dump(list(users), uf, indent=4)
    
    roles_to_save = []
    for role in roles:
        roles_to_save.append(role._asdict())
    
    bindings_to_save = []
    for binding in bindings:
        bindings_to_save.append(binding._asdict())

    with open('roles.json', 'w') as rf:
        json.dump(roles_to_save, rf, indent=4)

    with open('bindings.json', 'w') as bf:
        json.dump(bindings_to_save, bf, indent=4)
    
    with open('../opa/data.json', 'w') as df:
        data = DataObject(roles_to_save, bindings_to_save)
        json.dump(data._asdict(), df)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--roles', help='number of roles to generate', type=int, required=True)
    parser.add_argument('-u', '--users', help='number of users to generate', type=int, required=True)
    parser.add_argument('-b', '--bindings', help='number of bindings to generate between users and roles', type=int, required=True)
    args = parser.parse_args()
    main(args.roles, args.users, args.bindings)