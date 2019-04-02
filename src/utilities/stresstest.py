import json
import os
from random import choice
from subprocess import run
import argparse

class BindingsService():

    def __init__(self):
        self._load_users()
        self._load_roles()

    def _load_users(self):
        users_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')
        if not os.path.isfile(users_path):
            raise Exception('Not users.json file to load data from. Run the datagenerator.py file and then try again.')
        
        with open(users_path, 'r') as f:
            self.users = json.load(f)

    def _load_roles(self):
        roles_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roles.json')
        if not os.path.isfile(roles_path):
            raise Exception('Not roles.json file to load data from. Run the datagenerator.py file and then try again.')
        
        with open(roles_path, 'r') as f:
            self.roles = json.load(f)

    def get_random_user(self):
        return choice(self.users)

    def get_random_role(self):
        return choice(self.roles)

def update_input(binding_service):
    user = binding_service.get_random_user()
    role = binding_service.get_random_role()

    new_input = {
        "subject": {
            "user": user
        },
        "action": {
            "operation": role['operation'],
            "resource": role['resource']
        }
    }

    input_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'opa', 'input.json')
    with open(input_location, 'w') as f:
        json.dump(new_input, f)


def run_normal_eval():
    opa_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'opa')
    input_path = os.path.join(opa_dir, 'input.json')
    p = run(['opa', 'eval', '--data', opa_dir, '--input', input_path, '--metrics', 'data.example_rbac'], capture_output=True)
    return json.loads(p.stdout)

def run_partial_eval():
    # haven't quite worked out how to actually use the partial evaluation aspects of OPA just yet, hence why this isn't used
    p = run(['opa', 'eval', '--data', '../opa', '--input', '../opa/input.json', '--metrics', '--partial', 'data.example_rbac'], capture_output=True)
    return json.loads(p.stdout)

def main(trials):
    
    results = []
    bs = BindingsService()
    averages = {
        "timer_rego_module_compile_ns": 0,
        "timer_rego_module_parse_ns": 0,
        "timer_rego_query_compile_ns": 0,
        "timer_rego_query_eval_ns": 0,
        "timer_rego_query_parse_ns": 0
    }

    for _ in range(trials):
        update_input(bs)

        result = run_normal_eval()
        metrics = result['metrics']
        results.append(metrics)
        averages["timer_rego_module_compile_ns"] += metrics["timer_rego_module_compile_ns"] / trials
        averages["timer_rego_module_parse_ns"] += metrics["timer_rego_module_parse_ns"] / trials
        averages["timer_rego_query_compile_ns"] += metrics["timer_rego_query_compile_ns"] / trials
        averages["timer_rego_query_eval_ns"] += metrics["timer_rego_query_eval_ns"] / trials
        averages["timer_rego_query_parse_ns"] += metrics["timer_rego_query_parse_ns"] / trials
    

    save_data = {
        "averages": averages,
        "results": results
    }

    with open('results.json', 'w') as f:
        json.dump(save_data, f, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--trials', help='number of trials to run', type=int, required=True)
    args = parser.parse_args()
    main(args.trials)