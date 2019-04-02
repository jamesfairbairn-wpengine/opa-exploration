from collections import namedtuple

Role = namedtuple('Role', ['operation', 'resource', 'name'])

class Binding():

    def __init__(self, user, role):
        self.user = user
        self.role = role
    
    def __eq__(self, value):
        return value != None and self.user == value.user and self.role == value.role

    def __hash__(self):
        return f'{self.user}{self.role}'.__hash__()
        

DataObject = namedtuple('DataObject', ['roles', 'bindings'])