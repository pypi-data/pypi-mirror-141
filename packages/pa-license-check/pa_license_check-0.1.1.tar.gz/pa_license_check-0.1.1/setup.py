# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pa_license_check']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.4,<5.0',
 'click>=8.0.4,<9.0.0',
 'configparser>=5.2.0,<6.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.27.1,<3.0.0',
 'urllib3>=1.26.8,<2.0.0']

entry_points = \
{'console_scripts': ['palicensecheck = pa_license_check.cli:cli']}

setup_kwargs = {
    'name': 'pa-license-check',
    'version': '0.1.1',
    'description': 'Simple Script that logins to a Palo Alto firewall and checks license status\n to be used in conjunction with a monitoring software, like Nagios that reads exit codes',
    'long_description': '# Palo Alto License Check\n\nSimple script to be integrated into Icinga to alert the NOC team when firewall is set to expire in 60 days, 3 days or has already expired.\nThis was built as a solution where Palo Altos Panorama is not configured or to costly.\n\n## Installation\n\n##Using PIP\n\nThis package is uploaded to the PyPI and can be run as a command line program\n\n```bash\npip install pa-license-check\n```\n\nThis will install a CLI tool called \'palicensecheck\'. It will allow you to do the following\n\n1. Create an INI file that it uses to read the firewall\n2. Adds new clients to the INI File\n3. Checks the licensing status and returns an exit code\n\n##Using Poetry\n\nYou can install this by cloning the repo in Github and then using Poetry to install all the dependencies and setup the enviroment.\nYou can use this for development purposes if you wish to do so.\n\n1. Clone the project\n    1. Navigate to the root of the project directory\n2. Using Poetry run the following command\n    2. To install poetry [please see their page for further instructions](https://python-poetry.org/docs/)\n\n```bash\npoetry install\n```\n\n\n\n## How it works\n\nThe primary purpose for this script was as a stop gap between implementing Panorama and the lack of system expiration date from the SNMP MIBs that are included\nin Monitoring Software like LibreNMS.\n\nThe script makes an API call to the chosen firewall and parses through the XML its returned. It grabs the feature name and the expiration date.\nIt checks the expiration date against the current date. If the firewall expiration date is greater than 60 days, it returns a system code of 0 which indicates\nno errors. If the expiration date is within 60 days, it returns a system code of 1, prompting a warning. If the Expiration date is within 3 days, it returns a system code of 2, \nwhich indicates critical error. This will help give us visibility into the Palo Altos to ensure no firewall goes expired and without support from the vendor.\n\n60 days was chosen to allow ample time for Support or the Provisioning team to request a renewal quote and proceed through the Kissflow process.\n\n# Custom Exit Codes\n\nThe script utilizes a "Cusom Exit Code" to keep track of various states. This is not to be confused with the system exit codes, which are used to tell Icinga what severity.\nThis is strictly for keeping track within the function itself! I decided to Document it in case anyone wanted to expand on this.\n\n```text\nCustomExitCode is 0; Everything is ok\nCustomExitCode is 1; Warning, Hit 60 days\nCustomExitCode is 2; Warning, Coutning down from 60 days\nCustomExitCode is 3; Error, we are less than 3 days from expiration\nCustomExitCode is 4; We are past expiration date\n```\n\n# Running the script\n\n## Generating INI File\n\n\nOn the first initial run, you\'ll need to build the INI file. You can easily do this by running\n\n```bash\npalicensecheck create-ini-file\n```\n\nIt will then ask you a series of questions\n\n```text\nplease enter the firewall you wish to monitor\nhank.kingofthe.hill\nplease enter the Firewall Key\nwah5eeGhee7thah2waechohshai6ah6iphugh4ahpoophaeva0aeTutah6ohSooPopane\nPlease enter the clients name, I.E. ACME\nStrikland\n```\n\nIt will then create the INI file in the root directory of the script\nWhich will look like this.\n\n```text\n[strikland]\nkey = wah5eeGhee7thah2waechohshai6ah6iphugh4ahpoophaeva0aeTutah6ohSooPopane\nfw = hank.kingofthe.hill\n```\n\n## Adding clients to the INI file\n\nYou can easily add new clients to the INI file by running the following command\n\n```bash\npalicensecheck add-client-ini\n```\n\nIt will then walk you through a series of questions to help build the file.\n\n```bash\nplease enter the firewall you wish to monitor\nthatherton.fueles.demo\nplease enter the Firewall Key\noogoo1eec0ef0ong2ix0sheingughae8oongiebaicee3que0ShaD6rau0Looch9\nPlease enter the clients name, I.E. ACME\nthatherton\nfw_key.ini file appended with new information\n```\n\nhere we can see the expanded file\n\n```text\n[strikland]\nkey = wah5eeGhee7thah2waechohshai6ah6iphugh4ahpoophaeva0aeTutah6ohSooPopane\nfw = hank.kingofthe.hill\n[thatherton]\nkey = oogoo1eec0ef0ong2ix0sheingughae8oongiebaicee3que0ShaD6rau0Looch9\nfw = thatherton.fueles.demo\n```\n\n## Checking the license Status\n\nTo run the script and check the status, simply run the following command\n\n```bash\npalicensecheck check-license --client strikland\n```\n\nIts important to remember that the argument after the --client param **must** match the group name in your INI file.\n\n# To Do\n\nI cobbled this together to what it is today in a few hours time updating it.\nPlease let me know if there are bugs, issues or any features you would like added.\n\n* Testing against various firewalls\n* Implement API Automatic Key creation for easier deployment\n* Need to adjust some error catching\n\n\n',
    'author': 'Angelo Poggi',
    'author_email': 'angelo.poggi@opti9tech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/purplecomputer/pa_license_check',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
