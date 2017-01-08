#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.__init__.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Constructs specification
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

if __name__ == "__main__":
    __package__ = str("yspec.plugins")
    import yspec.plugins
from .. import YSpecCLTool


################################### CLASSES ###################################
class YSpecPlugin(YSpecCLTool):
    """
    Base class for YSpec plugins
    """
    annotate = True

    @classmethod
    def add_arguments(cls, parser, name=None, description=None, **kwargs):
        """
        Adds name and description of plugin to a nascent argument parser

        Arguments:
          parser (ArgumentParser): Parser to which arguments will be
            added
          name (str): Name of plugin
          description (str): Description of plugin
          kwargs (dict): Additional keyword arguments

        Returns:
          ArgumentParser: Argument parser
        """
        from .. import strfmt

        # Process arguments
        help_dest = kwargs.get("help_dest", parser)
        if name is None:
            if hasattr(cls, "name"):
                name = cls.name
            else:
                name = cls.__name__
        if description is None:
            if hasattr(cls, "description"):
                description = cls.description
            else:
                description = cls.__doc__

        # Add description of this plugin
        help_dest.description += "  {0}\n".format(name) + strfmt(description,
            width=79, initial_indent="    ", subsequent_indent="    ") + "\n"

        return parser

    @classmethod
    def get_config(cls, attr, constructor=None, attr_of_constructor=False,
            **kwargs):
        """
        """
        from .. import yaml_load

        if hasattr(cls, "name"):
            plugin_name = cls.name
        else:
            plugin_name = cls.__name__

        if kwargs.get(attr) is not None:
            return kwargs[attr]
        elif constructor is not None:
            if attr_of_constructor:
                if hasattr(constructor, attr):
                    return yaml_load(getattr(constructor, attr))
            else:
                if (hasattr(constructor,
                        "plugin_config") and plugin_name in
                    constructor.plugin_config):
                    config = yaml_load(constructor.plugin_config[plugin_name])
                    if attr in config:
                        return config[attr]
        return None

    def initialize(self, destination, key, comment=None):
        """
        Initializes a level within a nascent spec
        """
        from ruamel.yaml.comments import CommentedMap

        destination[key] = CommentedMap()
        if self.annotate:
            if comment is None:
                if hasattr(self, "name"):
                    comment = self.name
                else:
                    comment = self.__class__.__name__
            destination[key].yaml_add_eol_comment(comment, column=80)

    def set(self, destination, key, value, comment=None):
        """
        Sets a value within a nascent spec
        """
        from copy import deepcopy

        destination[key] = deepcopy(value)
        if self.annotate:
            if comment is None:
                if hasattr(self, "name"):
                    comment = self.name
                else:
                    comment = self.__class__.__name__
            destination.yaml_add_eol_comment(comment, key, column=80)
