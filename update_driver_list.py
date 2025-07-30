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

driver_list.sort()

print(driver_list)
with open("driver_list.txt", "w") as f:
    f.writelines(driver_list)

url = "https://raw.githubusercontent.com/FAU-LAP/CAMELS_drivers/driver_list/driver_list.txt"
online_driver_list = requests.get(url).text.splitlines()
online_drivers = []
online_versions = []
for i, d in enumerate(online_driver_list):
    val = d.strip().split("==")
    online_drivers.append(val[0])
    online_versions.append(val[1])

print("\n\n`Name`\t`Version in branch`\t`version on pypi`\t`version on driver list`")

for d in driver_list:
    name, version = d[:-1].split("==")
    last_v = get_latest_version(name)
    list_v = (
        online_versions[online_drivers.index(name)]
        if name in online_drivers
        else "None"
    )
    if version == last_v and version == list_v:
        sys.stdout.write(
            "\x1b[1;32m" + f"{name}\t{version}\t{last_v}\t{list_v}" + "\x1b[0m" + "\n"
        )
    else:
        sys.stdout.write(
            "\x1b[1;31m" + f"{name}\t{version}\t{last_v}\t{list_v}" + "\x1b[0m" + "\n"
        )
