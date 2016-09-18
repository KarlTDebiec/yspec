#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.SortPlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Sorts nascent spec
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("yspec.plugins")
    import yspec.plugins
from . import YSpecPlugin
################################### CLASSES ###################################
class SortPlugin(YSpecPlugin):
    """
    Sorts nascent spec

    Attributes
      name (str): Name of this plugin
      description (str): Description of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
    """
    name = "sort"
    description = """sorts nascent spec"""

    def __init__(self, indexed_levels=None, header=None, footer=None,
        constructor=None, **kwargs):
        """
        """
        from .. import yaml_load

        if indexed_levels is not None:
            self.indexed_levels = indexed_levels
        elif (constructor is not None
        and hasattr(constructor, "indexed_levels")):
            self.indexed_levels = yaml_load(constructor.indexed_levels)
        else:
            self.indexed_levels = {}

        if header is not None:
            self.header = header
        elif (constructor is not None
        and hasattr(constructor, "plugin_config")
        and "sort" in constructor.plugin_config
        and "header" in constructor.plugin_config["sort"]):
            self.header = yaml_load(
              constructor.plugin_config["sort"])["header"]
        else:
            self.header = []

        if footer is not None:
            self.footer = footer
        elif (constructor is not None
        and hasattr(constructor, "plugin_config")
        and "sort" in constructor.plugin_config
        and "footer" in constructor.plugin_config["sort"]):
            self.footer = yaml_load(
              constructor.plugin_config["sort"])["footer"]
        else:
            self.footer = []

    def __call__(self, spec, source_spec, **kwargs):
        """
        Adds default arguments to a nascent spec.

        Arguments:
          source_spec (CommentedMap): Nascent spec

        Returns:
          CommentedMap: Sorted spec
        """
        from ruamel.yaml.comments import CommentedMap

        source_spec = spec
        spec = CommentedMap()

        self.process_level(spec, source_spec, self.indexed_levels)
        return spec

    def process_level(self, spec, source_spec, indexed_levels):
        """
        Sorts one level of spec hierarchy

        Arguments:
          spec (CommentedMap): Nascent spec at current level
          source_spec (CommentedMap): Source spec at current level
        """

        # Process arguments
        if indexed_levels is None:
            indexed_levels = {}
        if source_spec is None:
            source_spec = {}

        # Loop over source argument keys and values at this level
        source_keys  = sorted([k for k in source_spec if k in self.header])
        source_keys += sorted([k for k in source_spec
                        if  k not in self.header
                        and k not in indexed_levels
                        and k not in self.footer])
        source_keys += sorted([k for k in source_spec if k in indexed_levels])
        source_keys += sorted([k for k in source_spec if k in self.footer])
        for source_key in source_keys:
            source_val = source_spec[source_key]
            # source_val is a dict; recurse
            if isinstance(source_val, dict):
                if source_key not in spec:
                    self.initialize(spec, source_key,
                      comment=source_val._yaml_comment.comment[0].value)
                if source_key in indexed_levels:
                    self.process_level(
                      spec[source_key],
                      source_spec.get(source_key, {}),
                      indexed_levels.get(source_key, {}))
                else:
                    self.process_level(
                      spec[source_key],
                      source_spec.get(source_key, {}),
                      indexed_levels)
            # source_val is singular; store and continue loop
            else:
                self.set(spec, source_key, source_val,
                  comment=source_spec._yaml_comment.items[source_key][2].value)
