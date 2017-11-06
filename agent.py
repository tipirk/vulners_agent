from pprint import pprint
from requests import post
from distro import linux_distribution
from platform import node
import subprocess
import json


def get_vuln(data_dict):
    query = json.dumps(data_dict)
    url = 'https://vulners.com/api/v3/audit/audit/'
    response = post(url, data=query).json()
    return response


def get_package_list(os_name):
    rpm_distros = ('rhel', 'redhat', 'suse', 'centos', 'fedora')
    dpkg_distros = ('debian', 'ubuntu')
    if os_name in rpm_distros:
        package_list_str = subprocess.run(['rpm', '-qa'],
                                          stdout=subprocess.PIPE).stdout
        package_list = package_list_str.decode().split('\n')
        del package_list[-1]
    elif os_name in dpkg_distros:
        package_list_str = subprocess.run(['dpkg-query', '-W',
                                           '-f="${Package} ${Version} '
                                           '${Architecture}\n"'],
                                          stdout=subprocess.PIPE).stdout
        package_list_raw = package_list_str.decode().split('"')
        package_list = []
        for i in range(len(package_list_raw) - 1):
            if package_list_raw[i] != '':
                package_list.append(package_list_raw[i][:-1])
    else:
        package_list = []
    return package_list


def get_os_info():
    os_name = linux_distribution()[0].lower()
    os_version = linux_distribution()[1].lower()
    return os_name, os_version


def get_hostname():
    hostname = node().lower()
    return hostname


if __name__ == "__main__":

    os_name, os_version = get_os_info()
    package_list = get_package_list(os_name)
    if package_list == []:
        print('Getting package list was failed')
    else:
        data_dict = {'os': os_name,
                     'version': os_version,
                     'package': package_list}
        vulners_info = get_vuln(data_dict)
        pprint(vulners_info['data']['packages'])
