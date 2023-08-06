from superqt.fonticon import icon
from fonticon_fa5 import FA5S, FA5B, FA5R
from qtpy.QtWidgets import QPushButton


def test_FA5S(qtbot):
    btn = QPushButton()
    qtbot.addWidget(btn)
    btn.setIcon(icon(FA5S.spinner))
    btn.show()

def test_FA5B(qtbot):
    btn = QPushButton()
    qtbot.addWidget(btn)
    btn.setIcon(icon(FA5B.accusoft))
    btn.show()

def test_FA5R(qtbot):
    btn = QPushButton()
    qtbot.addWidget(btn)
    btn.setIcon(icon(FA5R.address_book))
    btn.show()
