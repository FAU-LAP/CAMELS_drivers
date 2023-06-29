import pip
import tomllib
import os
import pkg_resources

driver_path = os.path.dirname(os.path.dirname(__file__))

try:
    with open('../driver_list.txt') as f:
        instr_list = [x.split('==')[0] for x in f.readlines()]
except:
    with open('driver_list.txt') as f:
        instr_list = [x.split('==')[0] for x in f.readlines()]

installed_packages = {pkg.key for pkg in pkg_resources.working_set}

for instr in instr_list:
    instr_path = f'{driver_path}/{instr}'
    toml_file = f'{instr_path}/pyproject.toml'
    if os.path.isfile(toml_file):
        with open(toml_file, 'rb') as toml_f:
            toml = tomllib.load(toml_f)
        if 'project' in toml and 'dependencies' in toml['project']:
            for d in toml['project']['dependencies']:
                if d in installed_packages:
                    continue
                pip.main(['install', d])
                installed_packages.add(d)