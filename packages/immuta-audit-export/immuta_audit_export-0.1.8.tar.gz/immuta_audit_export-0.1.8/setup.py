# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['immuta_audit_export',
 'immuta_audit_export.common',
 'immuta_audit_export.common.config_schemas',
 'immuta_audit_export.export_record',
 'immuta_audit_export.tenant_config']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.21.11,<2.0.0']

setup_kwargs = {
    'name': 'immuta-audit-export',
    'version': '0.1.8',
    'description': 'Scaffold for serverless audit exporting',
    'long_description': None,
    'author': 'LukeBoyer',
    'author_email': 'boyer.l@husky.neu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
