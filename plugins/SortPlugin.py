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
Sorts a nascent spec.
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
    Sorts a nascent spec.

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
    """
    name = "sort"
    description = """Sorts a nascent spec."""

    def __init__(self, **kwargs):
        """
        """
        pass

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

        self.process_level(spec, source_spec)
        return spec

    def process_level(self, spec, source_spec):
        """
        Sorts one level of spec hierarchy

        Arguments:
          spec (CommentedMap): Nascent spec at current level
          source_spec (CommentedMap): Source spec at current level
        """

        # Process arguments
        if source_spec is None:
            source_spec = {}

        # Loop over source argument keys and values at this level
        for source_key in sorted(source_spec):
            source_val = source_spec[source_key]
            # source_val is a dict; recurse
            if isinstance(source_val, dict):
                if source_key not in spec:
                    self.initialize(spec, source_key,
                      comment=source_val._yaml_comment.comment[0].value)
                self.process_level(
                  spec[source_key],
                  source_spec.get(source_key, {}))
            # source_val is singular; store and continue loop
            else:
                self.set(spec, source_key, source_val,
                  comment=source_spec._yaml_comment.items[source_key][2].value)
