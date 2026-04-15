"""Qt compatibility wrapper for PyQt6 / PySide6.

This module allows the app to import Qt from either binding.
If PyQt6 is available it is used first, otherwise PySide6 is used.
"""

try:
    from PyQt6 import QtCore, QtGui, QtWidgets
except ImportError:
    from PySide6 import QtCore, QtGui, QtWidgets
