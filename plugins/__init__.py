#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.__init__.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Constructs specification
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("yspec.plugins")
    import yspec.plugins
################################### CLASSES ###################################
class YSpecPlugin(object):
    """
    """
    name = ""
    annotate = True

    def initialize(self, destination, key, comment=None):
        """
        """
        from ruamel.yaml.comments import CommentedMap

        destination[key] = CommentedMap()
        if self.annotate:
            if comment is None:
                comment = self.name
            destination[key].yaml_add_eol_comment(self.name, column=80)

    def set(self, destination, key, value, comment=None):
        """
        """
        from copy import deepcopy

        destination[key] = deepcopy(value)
        if self.annotate:
            if comment is None:
                comment = self.name
            destination.yaml_add_eol_comment(self.name, key, column=80)

    @classmethod
    def construct_argparser(class_, parser, constructor=None, **kwargs):
        """
        Adds arguments to a nascent argument parser

        Arguments:
          parser (ArgumentParser): Parser to which arguments will be
            added
          constructor (YSpecConstructor): Constructor for which parser
            is being built
          kwargs (dict): Additional keyword arguments

        Returns:
          ArgumentParser: Argument parser
        """
        from .. import strfmt

        if ((constructor is not None)
        and (hasattr(constructor, "default_plugins"))
        and (class_.name in constructor.default_plugins)):
            parser.description += "  {0} (default: {1})\n".format(
              class_.name, constructor.default_plugins.index(class_.name))
        else:
            parser.description += "  {0}\n".format(class_.name)
        if hasattr(class_, "description"):
            parser.description += strfmt(class_.description , width=79,
              initial_indent="    ", subsequent_indent="    ") + "\n"

        return parser

