# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['canvas_workflow_helpers',
 'canvas_workflow_helpers.protocols',
 'canvas_workflow_helpers.tests',
 'canvas_workflow_helpers.value_sets',
 'canvas_workflow_helpers.value_sets.v2021']

package_data = \
{'': ['*'],
 'canvas_workflow_helpers.tests': ['mock_data/full_detailed_patient/*',
                                   'mock_data/no_details_patient/*',
                                   'mock_data/partial_detailed_patient/*',
                                   'mock_data/patient_appointments/patient_has_appointments/*',
                                   'mock_data/patient_appointments/patient_no_appointments/*',
                                   'mock_data/patient_contacts/multiple_contacts_73yo/*',
                                   'mock_data/patient_contacts/no_contacts_13yo/*',
                                   'mock_data/patient_contacts/no_contacts_72yo/*',
                                   'mock_data/patient_contacts/one_contact_73yo/*']}

install_requires = \
['arrow>=1.2.2,<2.0.0', 'canvas-workflow-kit>=0.4.5,<0.5.0']

setup_kwargs = {
    'name': 'canvas-workflow-helpers',
    'version': '0.1.0',
    'description': 'An open source project to empower customization of your Canvas instance using canvas-workflow-kit',
    'long_description': None,
    'author': 'Canvas Team',
    'author_email': 'engineering@canvasmedical.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
