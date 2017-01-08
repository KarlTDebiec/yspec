#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.CLArgumentPlugin.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Copies command line arguments to nascent spec
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

if __name__ == "__main__":
    __package__ = str("yspec.plugins")
    import yspec.plugins
from . import YSpecPlugin


################################### CLASSES ###################################
class CLArgumentPlugin(YSpecPlugin):
    """
    Copies command line arguments to nascent spec

    Attributes
      name (str): Name of this plugin
      description (str): Description of this plugin
    """
    name = "clargument"
    description = """copies command line arguments to nascent spec"""

    def __init__(self, **kwargs):
        """
        """
        exclude = self.get_config("exclude", **kwargs)
        if exclude is None:
            self.exclude = []
        else:
            self.exclude = exclude

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Copies command line arguments to nascent spec

        Arguments:
          spec (CommentedMap): Nascent spec
          kwargs (dict): Additional keyword arguments from command line

        Returns:
          CommentedMap: Updated spec including command line arguments
        """
        for cl_key, cl_val in kwargs.items():
            if cl_key not in self.exclude:
                if cl_val is not None:
                    self.set(spec, cl_key, cl_val, comment=self.name)
        return spec
