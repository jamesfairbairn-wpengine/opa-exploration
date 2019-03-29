# Setup

Ensure that you have the latest OPA cli tool downloaded and added to the path. The executable can be found [here](https://github.com/open-policy-agent/opa/releases/tag/v0.10.6).

# Executing

1. First run the `datagenerator.py` script in `scr/utilities`. This will create the files necessary for execution in the `stresstest.py`. It requires 3 parameters:
    * `-r` the number of roles to generate
    * `-u` the number of roles to generate
    * `-b` the number of bindings to generate
2. Now run the `stresstest.py` script with `-t` (the number of trials to run). Results will be output in the results.json file.