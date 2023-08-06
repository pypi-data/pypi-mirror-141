# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['fmri_physio_log']
install_requires = \
['pyparsing>=3.0.7,<4.0.0']

setup_kwargs = {
    'name': 'fmri-physio-log',
    'version': '0.2.0',
    'description': 'Parse Siemens PMU files',
    'long_description': '# fmri-physio-log\n\nParse Siemens PMU files\n\n[![PyPI Version](https://img.shields.io/pypi/v/fmri-physio-log.svg)](https://pypi.org/project/fmri-physio-log/) [![Tests](https://github.com/andrewrosss/fmri-physio-log/actions/workflows/unittests.yaml/badge.svg)](https://github.com/andrewrosss/fmri-physio-log/actions/workflows/unittests.yaml) [![Code Style](https://github.com/andrewrosss/fmri-physio-log/actions/workflows/linter.yaml/badge.svg)](https://github.com/andrewrosss/fmri-physio-log/actions/workflows/linter.yaml) [![Type Check](https://github.com/andrewrosss/fmri-physio-log/actions/workflows/type-check.yaml/badge.svg)](https://github.com/andrewrosss/fmri-physio-log/actions/workflows/type-check.yaml)\n\n## Installation\n\n```bash\npip install fmri-physio-log\n```\n\n## Overview\n\nThis small library parses and loads Siemens PMU files into python. These are `*.puls`, `*.resp`, `*.ecg` and `*.ext` files produced by the Siemens Physiological Monitoring Unit (PMU) which look something like:\n\n```text\n1 8 20 2 367 508 520 532 638 708 790 5000 1037 1108 1072 1190 1413 5003\nECG  Freq Per: 0 0\nPULS Freq Per: 72 823\nRESP Freq Per: 0 0\nEXT  Freq Per: 0 0\nECG  Min Max Avg StdDiff: 0 0 0 0\nPULS Min Max Avg StdDiff: 355 1646 795 5\nRESP Min Max Avg StdDiff: 0 0 0 0\nEXT  Min Max Avg StdDiff: 0 0 0 0\nNrTrig NrMP NrArr AcqWin: 0 0 0 0\nLogStartMDHTime:  36632877\nLogStopMDHTime:   39805825\nLogStartMPCUTime: 36632400\nLogStopMPCUTime:  39804637\n6003\n```\n\n## Usage\n\nBy default, `PhysioLog` takes a string as the only parameter:\n\n```python\nimport fmri_physio_log as fpl\n\nCONTENT = """\\\n1 8 20 2 5002 LOGVERSION 102 6002 5002 TRIGGERMETHOD 10 6002 367 508 520 532 638 708 790 5000 1037 1108 5002\n data that spans multiple lines ...\n6002 1072 1190 1413 5003\nECG  Freq Per: 0 0\nPULS Freq Per: 72 823\nRESP Freq Per: 0 0\nEXT  Freq Per: 0 0\nECG  Min Max Avg StdDiff: 0 0 0 0\nPULS Min Max Avg StdDiff: 355 1646 795 5\nRESP Min Max Avg StdDiff: 0 0 0 0\nEXT  Min Max Avg StdDiff: 0 0 0 0\nNrTrig NrMP NrArr AcqWin: 0 0 0 0\nLogStartMDHTime:  36632877\nLogStopMDHTime:   39805825\nLogStartMPCUTime: 36632400\nLogStopMPCUTime:  39804637\n6003\n"""\n\nlog = fpl.PhysioLog(CONTENT)\n\nlog.ts  # [367, 508, 520, 532, 638, 708, 790, 1037, 1108, 1072, 1190, 1413]\nlog.rate  # 20\nlog.params  # (1, 8, 20, 2)\nlog.info  # [\'LOGVERSION 102\', \'TRIGGERMETHOD 10\', \'data that spans multiple lines ...\']\n\nlog.ecg  # MeasurementSummary(freq=0, per=0, min=0, max=0, avg=0, std_diff=0)\nlog.puls  # MeasurementSummary(freq=72, per=823, min=355, max=1646, avg=795, std_diff=5)\nlog.resp  # MeasurementSummary(freq=0, per=0, min=0, max=0, avg=0, std_diff=0)\nlog.ext  # MeasurementSummary(freq=0, per=0, min=0, max=0, avg=0, std_diff=0)\n\nlog.nr  # NrSummary(nr_trig=0, nr_m_p=0, nr_arr=0, acq_win=0)\n\nlog.mdh  # LogTime(start=36632877, stop=39805825)\nlog.mpcu  # LogTime(start=36632400, stop=39804637)\n\n# For convenience the start and stop times are available\n# as python datetime.time objects as well\nlog.mdh.start_time  # datetime.time(10, 10, 32, 877000)\nlog.mdh.stop_time  # datetime.time(11, 3, 25, 825000)\nlog.mpcu.start_time  # datetime.time(10, 10, 32, 400000)\nlog.mpcu.stop_time  # datetime.time(11, 3, 24, 637000)\n```\n\n### From an open file\n\nA `PhysioLog` object can also be instantiated from an open file\n\n```python\nimport fmri_physio_log as fpl\n\nwith open("sample.puls", "r") as f:\n    log = fpl.PhysioLog.from_file(f)\n```\n\n### From a path\n\nA `PhysioLog` object can also be instantiated from a file path (either as a string or a `pathlib.Path` object)\n\n```python\nfrom pathlib import Path\n\nimport fmri_physio_log as fpl\n\n# path as string\npath_s = "/path/to/my/file.resp"\nlog = fpl.PhysioLog.from_filename(path_s)\n\n# path as pathlib.Path object\npath = Path(path_s)\nlog = fpl.PhysioLog.from_filename(path)\n```\n\n## Implementation References\n\nThe following sources were referenced in constructing the grammar:\n\n- [https://cfn.upenn.edu/aguirre/wiki/doku.php?id=public:pulse-oximetry_during_fmri_scanning#pulse-ox_data](https://cfn.upenn.edu/aguirre/wiki/doku.php?id=public:pulse-oximetry_during_fmri_scanning#pulse-ox_data)\n- [https://wiki.humanconnectome.org/display/PublicData/Understanding+Timing+Information+in+HCP+Physiological+Monitoring+Files](https://wiki.humanconnectome.org/display/PublicData/Understanding+Timing+Information+in+HCP+Physiological+Monitoring+Files)\n- [https://gitlab.ethz.ch/physio/physio-doc/-/wikis/MANUAL_PART_READIN#manual-recording](https://gitlab.ethz.ch/physio/physio-doc/-/wikis/MANUAL_PART_READIN#manual-recording)\n- [https://gist.github.com/rtrhd/6172344](https://gist.github.com/rtrhd/6172344)\n\n## Contributing\n\n1. Have or install a recent version of `poetry` (version >= 1.1)\n1. Fork the repo\n1. Setup a virtual environment (however you prefer)\n1. Run `poetry install`\n1. Run `pre-commit install`\n1. Add your changes (adding/updating tests is always nice too)\n1. Commit your changes + push to your fork\n1. Open a PR\n',
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andrewrosss/fmri-physio-log',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
