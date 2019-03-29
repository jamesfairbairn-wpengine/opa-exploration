from collections import namedtuple

Role = namedtuple('Role', ['operation', 'resource', 'name'])
Binding = namedtuple('Binding', ['user', 'role'])

DataObject = namedtuple('DataObject', ['roles', 'bindings'])