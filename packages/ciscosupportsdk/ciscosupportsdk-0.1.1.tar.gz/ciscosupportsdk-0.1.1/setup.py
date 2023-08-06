# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ciscosupportsdk', 'ciscosupportsdk.api', 'ciscosupportsdk.models']

package_data = \
{'': ['*']}

install_requires = \
['Authlib>=0.15.5,<0.16.0', 'pydantic>=1.9.0,<2.0.0', 'requests>=2.27.1,<3.0.0']

setup_kwargs = {
    'name': 'ciscosupportsdk',
    'version': '0.1.1',
    'description': 'Cisco Support APIs allow Cisco Partner Support Services (PSS) partners and Cisco Smart Net Total Care (SNTC) customers to programmatically access and consume Cisco Support data in the cloud in a simple, secure, and scalable manner.',
    'long_description': "ciscosupportsdk\n===============\n\nPython API wrapper for the Cisco Support APIs.\n\n|docs| |tests| |coverage|\n----------------------------------------------\n\nThe **ciscosupportsdk** supports all of the Cisco Support API\ninteractions via a native Python library.  This makes working with\nthese APIs a more *natural* experience and eases the burden of writing\nyour own boilerplate code to deal with API semantics, like authentication\nand pagination.\n\nQuick Usage\n-----------\n.. code-block:: Python\n\n   from ciscosupportsdk.api import CiscoSupportAPI\n\n   api = CiscoSupportAPI(CS_API_KEY, CS_API_SECRET)\n\n   # find if a serial number is covered and when it's warranty expires\n   for item in api.serial_information.get_coverage_status(['FXS2130Q286']):\n      print(f'{item.is_covered} {item.warranty_end_date}')\n\n\n.. |docs| image:: https://github.com/supermanny81/ciscosupportapi/actions/workflows/docs_to_pages.yaml/badge.svg \n   :target: https://github.com/supermanny81/ciscosupportapi/actions/workflows/docs_to_pages.yaml\n.. |coverage| image:: https://codecov.io/gh/supermanny81/ciscosupportapi/branch/master/graph/badge.svg?token=CU4V95TVF1\n   :target: https://codecov.io/gh/supermanny81/ciscosupportapi\n.. |tests| image:: https://github.com/supermanny81/ciscosupportapi/actions/workflows/test.yaml/badge.svg\n   :target: https://github.com/supermanny81/ciscosupportapi/actions/workflows/test.yaml",
    'author': 'Manny Garcia',
    'author_email': 'supermanny@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://supermanny81.github.io/ciscosupportapi/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
