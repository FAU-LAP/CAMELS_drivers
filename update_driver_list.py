import os.path
import pathlib
import tomllib
import subprocess
import sys

def get_latest_version(instr):
    latest_version = str(subprocess.run([sys.executable, '-m', 'pip', 'install', f'nomad-camels-driver-{instr.replace("_", "-")}==random'], capture_output=True, text=True))
    latest_version = latest_version[latest_version.find('(from versions:')+15:]
    latest_version = latest_version[:latest_version.find(')')]
    return latest_version.replace(' ','').split(',')[-1]

driver_list = []

for f in pathlib.Path(os.path.dirname(__file__)).rglob('pyproject.toml'):
    if '.desertenv' in str(f):
        continue
    with open(f, 'rb') as toml_f:
        toml = tomllib.load(toml_f)
    if 'project' in toml:
        toml_proj = toml['project']
        name = ''
        if 'name' in toml_proj:
            name = toml_proj['name'].split("nomad_camels_driver_")[-1]
        version = ''
        if 'version' in toml_proj:
            version = toml_proj['version']
        if name and version:
            driver_list.append(f'{name}=={version}\n')

print(driver_list)
with open('driver_list.txt', 'w') as f:
    f.writelines(driver_list)


for d in driver_list:
    name, version = d[:-1].split('==')
    last_v = get_latest_version(name)
    if version == last_v:
        sys.stdout.write('\x1b[1;32m' + f'{name}\t{version}\t{last_v}' + '\x1b[0m' + '\n')
    else:
        sys.stdout.write('\x1b[1;31m' + f'{name}\t{version}\t{last_v}' + '\x1b[0m' + '\n')
