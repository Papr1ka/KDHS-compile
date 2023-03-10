from kivy.core.window import Window
from kivy.properties import StringProperty, NumericProperty, ColorProperty

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import BaseSnackbar


class ExtendedBaseSnackbar(BaseSnackbar):
    pass


class ErrorSnackbar(ExtendedBaseSnackbar):
    text = StringProperty("")


class SuccessSnackbar(ExtendedBaseSnackbar):
    text = StringProperty("")


def show_error_snackbar(text, *args, **kwargs):
    ErrorSnackbar(text=text).open()

def show_success_snackbar(text, *args, **kwargs):
    SuccessSnackbar(text=text).open()
