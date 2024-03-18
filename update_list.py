import requests


def get_latest_version(package_name):
    name = f'nomad-camels-driver-{package_name.replace("_", "-")}'
    response = requests.get(f"https://pypi.org/pypi/{name}/json")
    return response.json()["info"]["version"]


with open("driver_list.txt", "r") as file:
    lines = file.readlines()

with open("driver_list.txt", "w") as file:
    for line in lines:
        package_name, _ = line.split("==")
        latest_version = get_latest_version(package_name)
        file.write(f"{package_name}=={latest_version}\n")
