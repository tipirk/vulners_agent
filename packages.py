from pprint import pprint
import subprocess
import requests
import json
import distro


def get_vuln(data_dict):
    query = json.dumps(data_dict)
    url = 'https://vulners.com/api/v3/audit/audit/'
    response = requests.post(url, data=query).json()
    return response


def get_package_list():
    package_list_str = subprocess.run(['rpm', '-qa'],
                                      stdout=subprocess.PIPE).stdout
    package_list = package_list_str.decode().split('\n')
    del package_list[-1]
    return package_list


def get_os_info():
    os_name = distro.linux_distribution()[0]
    os_version = distro.linux_distribution()[1]
    return os_name, os_version


# package_list = get_package_list()
os_name = get_os_info()[0]
os_version = get_os_info()[1]
# data_dict = {'os': os_name, 'version': os_version, 'package': package_list}

# vulners_info = get_vuln(data_dict)
# pprint(vulners_info['data']['packages'])
print(os_name)
print(os_version)
