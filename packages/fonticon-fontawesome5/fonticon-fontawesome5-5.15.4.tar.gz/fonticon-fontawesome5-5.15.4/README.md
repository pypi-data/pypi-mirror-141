# fonticon-fontawesome5

[![License](https://img.shields.io/pypi/l/fonticon-fontawesome5.svg?color=green)](https://github.com/tlambert03/fonticon-fontawesome5/raw/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/fonticon-fontawesome5.svg?color=green)](https://pypi.org/project/fonticon-fontawesome5)
[![Python Version](https://img.shields.io/pypi/pyversions/fonticon-fontawesome5.svg?color=green)](https://python.org)
[![CI](https://github.com/tlambert03/fonticon-fontawesome5/workflows/ci/badge.svg)](https://github.com/tlambert03/fonticon-fontawesome5/actions)
[![codecov](https://codecov.io/gh/tlambert03/fonticon-fontawesome5/branch/master/graph/badge.svg)](https://codecov.io/gh/tlambert03/fonticon-fontawesome5)

FontAwesome 5 extension for superqt font icons

```sh
pip install superqt fonticon-fontawesome5
```

```python

from fonticon_fa5 import FA5S
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QApplication, QPushButton
from superqt.fonticon import icon, pulse

app = QApplication([])

btn2 = QPushButton()
btn2.setIcon(icon(FA5S.spinner, animation=pulse(btn2)))
btn2.setIconSize(QSize(225, 225))
btn2.show()

app.exec_()
```
