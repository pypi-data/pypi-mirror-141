# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['physicool']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.5.1,<4.0.0',
 'numpy>=1.22.2,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'scipy>=1.8.0,<2.0.0',
 'seaborn>=0.11.2,<0.12.0']

setup_kwargs = {
    'name': 'physicool',
    'version': '0.1.0',
    'description': 'A generalized, model-agnostic framework for model calibration in PhysiCell.',
    'long_description': '# PhysiCOOL: A generalized framework for model Calibration and Optimization Of modeLing projects\n\n![GitHub](https://img.shields.io/github/license/iggoncalves/PhysiCOOL)\n[![Documentation Status](https://readthedocs.org/projects/physicool/badge/?version=latest)](https://physicool.readthedocs.io/en/latest/?badge=latest)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/IGGoncalves/PhysiCOOL/HEAD?urlpath=%2Ftree%2Fexamples)\n\nPhysiCOOL aims to be a generalized framework for **model calibration in PhysiCell**. PhysiCell projects can be used a **black-box** to characterize how the model outputs change in response to variations in the input values. With this in mind, PhysiCOOL introduces a **model-agnostic calibration workflow** that easily integrates with PhysiCell models, and that allows users to **find the best set of parameters for their study**.\n\nPhysiCOOL provides new functions that allow users to easily specify the parameters to vary, as well as the metrics to be quantified (i.g., number of cells through time, total traveled distance,...). Check our [documentation](https://physicool.readthedocs.io) for some examples.\n\n## Instalation\n\nPhysiCOOL is available through pip. You can download it with the following command:\n\n```sh\npip install physicool\n```\n\n## Usage\n\n### PhysiCell as a black-box model\n\nPhysiCOOL lets you connect PhysiCell models to Python-based parameter estimation and calibration scripts. To do this, PhysiCOOL helps you convert PhysiCell models into a black-box function that implements the workflow presented below:\n\n```mermaid\ngraph LR\n    START[Input values] -->|Update config file| B(Run PhysiCell)\n    B --> |Process results| C[Output value]\n```\n\nBoth the functions that update the config file and that process the results data can be defined by the user.\n\n### 🏗️ Multilevel parameter sweep\n\nThe `MultiSweep` class will let you run a **multilevel parameter sweep in which the parameter bounds are iteratively adapted based on the minimum value found at each level**. To create it, you must **select the model you want to run at each level** as well as the **target data** you want to use. Additionally, you can tune the **number of levels**, and the **number of points and ranges to explore at each level**. Additionally, you can define parameter bounds.\n\n### Other utilities\n\nPhysiCOOL implements a file parser (`ConfigFileParser`) that lets you read and write data to the PhysiCell XML configuration file with simple Python commands.\n\n## Examples\n\nYou can run our examples on [Binder](https://mybinder.org/v2/gh/IGGoncalves/PhysiCOOL/HEAD?urlpath=%2Ftree%2Fexamples)!\n\n- **Interactive parameter estimation example:**\nGuides you through a simple example of logistic growth to showcase how the multilevel sweep works.\n\n- 🏗️ **Single-cell motility:**\nStudies the effect of the migration bias and migration speed in the presence of a chemotactic gradient.\n\n- 🏗️ **Cell growth:**\nStudies the effect of the cell cycling rates on population growth. It also introduces gradient-based approaches.\n\n- 🏗️ **Data analysis and visualization:**\nExamples of data visualization scripts, including interactive examples with Jupyter Widgets.\n\n## Team\n\nTool developed by Inês Gonçalves, David Hormuth, Caleb Phillips, Sandhya Prabhakaran. Runner-up team of the "Best Tool" prize at [PhysiCell 2021 Workshop & Hackaton](http://physicell.org/ws2021/#apply). GO TEAM 7!\n\n## Credits\n\n`PhysiCOOL` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Inês Gonçalves, David Hormuth, Caleb Phillips, Sandhya Prabhakaran',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
