#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import path
import sys


def resource_path(relative_path):
    """
    In order to find the files associated with the tool,
    this function returns the needed path
    :param relative_path:
    :return: String
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)