# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xaitk_saliency',
 'xaitk_saliency.impls',
 'xaitk_saliency.impls.gen_classifier_conf_sal',
 'xaitk_saliency.impls.gen_descriptor_sim_sal',
 'xaitk_saliency.impls.gen_detector_prop_sal',
 'xaitk_saliency.impls.gen_image_classifier_blackbox_sal',
 'xaitk_saliency.impls.perturb_image',
 'xaitk_saliency.interfaces',
 'xaitk_saliency.utils',
 'xaitk_saliency.utils.bin']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'numpy>=1.20.3,<2.0.0',
 'scikit-image>=0.18.1,<0.19.0',
 'scikit-learn>=0.24.2,<0.25.0',
 'scipy>=1.6.3,<2.0.0',
 'smqtk-classifier>=0.17.0',
 'smqtk-core>=0.18.0',
 'smqtk-descriptors>=0.16.0',
 'smqtk-detection>=0.18.1']

extras_require = \
{'example_deps': ['jupyter>=1.0.0,<2.0.0',
                  'matplotlib>=3.4.1,<4.0.0',
                  'papermill>=2.3.3,<3.0.0',
                  'torch>=1.9.0,<2.0.0',
                  'torchvision>=0.10.0,<0.11.0',
                  'tqdm>=4.45.0,<5.0.0'],
 'tools': ['kwcoco>=0.2.18,<0.3.0']}

entry_points = \
{'console_scripts': ['sal-on-coco-dets = '
                     'xaitk_saliency.utils.bin.sal_on_coco_dets:sal_on_coco_dets'],
 'smqtk_plugins': ['impls.gen_classifier_conf_sal.occlusion_scoring = '
                   'xaitk_saliency.impls.gen_classifier_conf_sal.occlusion_scoring',
                   'impls.gen_classifier_conf_sal.rise_scoring = '
                   'xaitk_saliency.impls.gen_classifier_conf_sal.rise_scoring',
                   'impls.gen_descriptor_sim_sal.similarity_scoring = '
                   'xaitk_saliency.impls.gen_descriptor_sim_sal.similarity_scoring',
                   'impls.gen_detector_prop_sal.drise_scoring = '
                   'xaitk_saliency.impls.gen_detector_prop_sal.drise_scoring',
                   'impls.gen_image_classifier_blackbox_sal.occlusion_based = '
                   'xaitk_saliency.impls.gen_image_classifier_blackbox_sal.occlusion_based',
                   'impls.gen_image_classifier_blackbox_sal.rise = '
                   'xaitk_saliency.impls.gen_image_classifier_blackbox_sal.rise',
                   'impls.perturb_image.rise = '
                   'xaitk_saliency.impls.perturb_image.rise',
                   'impls.perturb_image.sliding_radial = '
                   'xaitk_saliency.impls.perturb_image.sliding_radial',
                   'impls.perturb_image.sliding_window = '
                   'xaitk_saliency.impls.perturb_image.sliding_window']}

setup_kwargs = {
    'name': 'xaitk-saliency',
    'version': '0.5.0',
    'description': 'Visual saliency map generation interfaces and baseline implementations for explainable AI.',
    'long_description': '![xaitk-logo](./docs/figures/xaitk-wordmark.png)\n\n<hr/>\n\n[![PyPI - Python Version](https://img.shields.io/pypi/v/xaitk-saliency)](https://pypi.org/project/xaitk-saliency/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/xaitk-saliency)\n[![Documentation Status](https://readthedocs.org/projects/xaitk-saliency/badge/?version=latest)](https://xaitk-saliency.readthedocs.io/en/latest/?badge=latest)\n[![badge-unittests](https://github.com/xaitk/xaitk-saliency/actions/workflows/ci-unittests.yml/badge.svg)](https://github.com/XAITK/xaitk-saliency/actions/workflows/ci-unittests.yml)\n[![badge-notebooks](https://github.com/xaitk/xaitk-saliency/actions/workflows/ci-example-notebooks.yml/badge.svg)](https://github.com/XAITK/xaitk-saliency/actions/workflows/ci-example-notebooks.yml)\n[![codecov](https://codecov.io/gh/XAITK/xaitk-saliency/branch/master/graph/badge.svg?token=VHRNXYCNCG)](https://codecov.io/gh/XAITK/xaitk-saliency)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/XAITK/xaitk-saliency.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/XAITK/xaitk-saliency/context:python)\n\n# XAITK - Saliency\nThe `xaitk-saliency` package is an open source, Explainable AI (XAI) framework\nfor visual saliency algorithm interfaces and implementations, built for\nanalytics and autonomy applications.\n\nSee [here](https://xaitk-saliency.readthedocs.io/en/latest/introduction.html)\nfor a more formal introduction to the topic of XAI and visual saliency\nexplanations.\n\nThis framework is a part of the [Explainable AI Toolkit (XAITK)](\nhttps://xaitk.org).\n\n## Target Audience\nThis toolkit is intended to help data scientists and developers who want to\nadd visual saliency explanations to their workflow or product.\nFunctionality provided here is both directly accessible for targeted\nexperimentation, and through [Strategy](\nhttps://en.wikipedia.org/wiki/Strategy_pattern) and [Adapter](\nhttps://en.wikipedia.org/wiki/Adapter_pattern) patterns to allow for\nmodular integration into systems and applications.\n\n## Installation\nInstall the latest release via pip:\n```bash\npip install xaitk-saliency\n```\n\nSome plugins may require additional dependencies in order to be utilized at\nruntime.\nSuch details are described [here](\nhttps://xaitk-saliency.readthedocs.io/en/latest/implementations.html).\n\nSee [here for more installation documentation](\nhttps://xaitk-saliency.readthedocs.io/en/latest/installation.html).\n\n## Getting Started\nWe provide a number of examples based on Jupyter notebooks in the `./examples/`\ndirectory to show usage of the `xaitk-saliency` package in a number of\ndifferent contexts.\n\nContributions are welcome!\nSee the [CONTRIBUTING.md](./CONTRIBUTING.md) file for details.\n\n## Documentation\nDocumentation snapshots for releases as well as the latest master are hosted on\n[ReadTheDocs](https://xaitk-saliency.readthedocs.io/en/latest/).\n\nThe sphinx-based documentation may also be built locally for the most\nup-to-date reference:\n```bash\n# Install dependencies\npoetry install\n# Navigate to the documentation root.\ncd docs\n# Build the docs.\npoetry run make html\n# Open in your favorite browser!\nfirefox _build/html/index.html\n```\n',
    'author': 'Kitware, Inc.',
    'author_email': 'xaitk@kitware.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/XAITK/xaitk-saliency',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
