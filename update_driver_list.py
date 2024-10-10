import os.path
import pathlib
import toml as tomllib
import sys

import requests


def get_latest_version(package_name):
    name = f'nomad-camels-driver-{package_name.replace("_", "-")}'
    response = requests.get(f"https://pypi.org/pypi/{name}/json")
    if response.status_code != 200:
        return "None"
    return response.json()["info"]["version"]



driver_list = []

for f in pathlib.Path(os.path.dirname(__file__)).rglob("pyproject.toml"):
    if ".desertenv" in str(f) or ".venv" in str(f):
        continue
    toml = tomllib.load(f)
    if "project" in toml:
        toml_proj = toml["project"]
        name = ""
        if "name" in toml_proj:
            name = toml_proj["name"].split("nomad_camels_driver_")[-1]
        version = ""
        if "version" in toml_proj:
            version = toml_proj["version"]
        if name and version:
            driver_list.append(f"{name}=={version}\n")

print(driver_list)
with open("driver_list.txt", "w") as f:
    f.writelines(driver_list)


for d in driver_list:
    name, version = d[:-1].split("==")
    last_v = get_latest_version(name)
    if version == last_v:
        sys.stdout.write(
            "\x1b[1;32m" + f"{name}\t{version}\t{last_v}" + "\x1b[0m" + "\n"
        )
    else:
        sys.stdout.write(
            "\x1b[1;31m" + f"{name}\t{version}\t{last_v}" + "\x1b[0m" + "\n"
        )
