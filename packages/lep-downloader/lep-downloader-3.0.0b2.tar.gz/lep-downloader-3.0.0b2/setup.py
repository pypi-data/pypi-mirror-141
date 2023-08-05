# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lep_downloader', 'lep_downloader.commands']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0',
 'click>=8.0.4,<9.0.0',
 'loguru>=0.6.0,<0.7.0',
 'lxml>=4.6.3,<5.0.0',
 'requests>=2.26.0,<3.0.0',
 'single-source>=0.2.0,<0.3.0']

entry_points = \
{'console_scripts': ['lep-dl = lep_downloader.__main__:main',
                     'lep-downloader = lep_downloader.__main__:main']}

setup_kwargs = {
    'name': 'lep-downloader',
    'version': '3.0.0b2',
    'description': "LEP Downloader - CLI app for parsing and downloading episodes of Luke's English Podcast",
    'long_description': "LEP Downloader\n==============\n\n.. badges-begin\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/lep-downloader.svg\n   :target: https://pypi.org/project/lep-downloader/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/lep-downloader.svg\n   :target: https://pypi.org/project/lep-downloader/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/lep-downloader\n   :target: https://pypi.org/project/lep-downloader\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/lep-downloader\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/lep-downloader/latest.svg?label=Read%20the%20Docs\n   :target: https://lep-downloader.readthedocs.io/\n   :alt: Read the documentation at https://lep-downloader.readthedocs.io/\n.. |Tests| image:: https://github.com/hotenov/lep-downloader/workflows/Tests/badge.svg\n   :target: https://github.com/hotenov/lep-downloader/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/hotenov/lep-downloader/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/hotenov/lep-downloader\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n=========\n\n.. badges-end\n\n.. after-image\n\nAbout\n------\n\nLEP Downloader is a script for downloading the all FREE episodes of `Luke's ENGLISH Podcast`_.\n\nIt lets you to get all audio files (including audio tracks to video episodes)\nand also PDF files for each episode page.\n\nEven though this script was written for convenient episode downloading,\nI don't want to financially harm Luke in any way.\nI just want to make my life a bit easier (as usual for lazy IT person =).\nSo consider `donating`_ to Luke's English Podcast and `becoming`_ his premium subscriber.\nAnd of course, subscribe on his `YouTube channel`_.\n\n`Read the full documentation <https://lep-downloader.readthedocs.io>`__ on website.\n\n🚀 Features\n-------------\n\n* Download a range of episodes filtering by episode number or by episode date\n* Download only the last episode\n* Download PDF files of episodes web pages\n* Saving files to specified folder on your hard / solid / flash drive\n* Running script in quiet mode for automated routine\n* Writing log file in debug mode\n\n\n🛠️ Requirements\n----------------\n\n* Python 3.8+\n* Internet connection\n\n\n💻 Installation\n----------------\n\nYou can install *LEP Downloader* via pip_ from PyPI_:\n\n.. code:: none\n\n   pip install lep-downloader\n\nI do recommend you to use pipx_ for any CLI Python package.\nIt let you install and run Python applications in isolated environments.\n\n.. code:: none\n\n   python -m pip install --user pipx\n   pipx install lep-downloader\n   lep-downloader --help\n\n\n🕹 Usage\n--------\n\n.. code:: none\n\n   lep-downloader -ep 758\n\nYou can also use the short script name:\n\n.. code:: none\n\n   lep-dl --last\n\nPlease see the `Usage Examples <Usage_>`_ for details.\n\nOr skim the `Man Page <Manpage_>`_ for available options\n(if terminal is your best friend).\n\n\n✨ What's new in version 3\n---------------------------\n\nThe third version was completely re-written by me (again).\nBut this time with more fundamental and mature approach.\nI applied some OOP (object-oriented programming) principles\nand covered almost all functions with absolutely isolated unit tests.\n\nCode base became more extendable and maintainable *(I believe)*.\nI dropped support for file naming from old script versions.\nAlso I removed (for awhile) video and add-ons download\n*(I plan to add them again in the future, however - no any promises)*.\n\nArchive parsing was improved (without skipping several episodes).\nAlso I added built-in possibility to download files from reserve server,\nif primary link is not available (for any reason).\n\nAnd many internal little things.\nYou can read descriptions of pre-releases on `Releases`_ page (if you wish).\n\n\n✊ Contributing\n---------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\n📝 License\n-----------\n\nDistributed under the terms of the `MIT license <https://opensource.org/licenses/MIT>`_,\n*LEP Downloader* is free and open source software.\nIt means you can modify it, redistribute it or use it however you like\nas long as you do mention the author of the original script.\n\n\n🐞 Issues\n----------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\n🙏🏻 Credits\n------------\n\nThis project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.\n\nScript uses the following packages / libraries under the hood:\n\n* `click <https://github.com/pallets/click>`_ (`BSD-3-Clause License <https://github.com/pallets/click/blob/main/LICENSE.rst>`__)\n* `requests <https://github.com/psf/requests>`_ (`Apache-2.0 License <https://github.com/psf/requests/blob/main/LICENSE>`__)\n* `beautifulsoup4 <https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html>`_ (`MIT License <https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/LICENSE>`__)\n* `lxml <https://github.com/lxml/lxml>`_ (`BSD-3-Clause License <https://github.com/lxml/lxml/blob/master/LICENSE.txt>`__)\n* `loguru <https://github.com/Delgan/loguru>`_ (`MIT License <https://github.com/Delgan/loguru/blob/master/LICENSE>`__)\n* `single-source <https://github.com/rabbit72/single-source>`_ (`MIT License <https://github.com/rabbit72/single-source/blob/master/LICENSE>`__)\n\nand other amazing Python packages for development and testing.\nSee a full list of them in 'dependencies' section of ``pyproject.toml``\n`file <https://github.com/hotenov/LEP-downloader/blob/main/pyproject.toml>`_.\n\n.. _Luke's ENGLISH Podcast: https://teacherluke.co.uk/archive-of-episodes-1-149/\n.. _donating: https://www.paypal.com/donate/?cmd=_s-xclick&hosted_button_id=CA2KNZNBFGKC6\n.. _becoming: https://teacherluke.co.uk/premium/premiuminfo/\n.. _YouTube channel: https://www.youtube.com/c/LukesEnglishPodcast\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/hotenov/lep-downloader/issues\n.. _pip: https://pip.pypa.io/\n.. _pipx: https://pipxproject.github.io/pipx/\n.. _Releases: https://github.com/hotenov/LEP-downloader/releases\n\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://lep-downloader.readthedocs.io/en/latest/usage.html\n.. _Manpage: https://lep-downloader.readthedocs.io/en/latest/manpage.html\n",
    'author': 'Artem Hotenov',
    'author_email': 'qa@hotenov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hotenov/LEP-downloader',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)
