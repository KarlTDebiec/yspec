#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.InitializePlugin.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Initializes a nascent spec.
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

if __name__ == "__main__":
    __package__ = str("yspec.plugins")
    import yspec.plugins
from . import YSpecPlugin


################################### CLASSES ###################################
class InitializePlugin(YSpecPlugin):
    """
    Initializes a nascent spec.

    Attributes
      name (str): Name of this plugin
      description (str): Description of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
    """
    name = "initialize"
    description = """initializes indexed levels of nascent spec based on
      source spec"""

    def __init__(self, **kwargs):
        """
        """
        self.indexed_levels = self.get_config("indexed_levels",
          attr_of_constructor=True, **kwargs)

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Initializes a nascent spec.

        Arguments:
          spec (CommentedMap): Nascent spec (typically empty at this time)
          source_spec (dict): Source spec to use to determine initial
            structure

        Returns:
          CommentedMap: Initialized spec
        """
        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels)
        return spec

    def process_level(self, spec, source_spec, indexed_levels, path=None):
        """
        Initializes one level of spec hierarchy

        Arguments:
          spec (CommentedMap): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels below current level
          path (list): List of keys leading to this level
        """

        # Process arguments
        if indexed_levels is None or source_spec is None:
            return
        if path is None:
            path = []

        # Loop over indexed levels at this level
        for level in [k for k in indexed_levels if k in source_spec]:
            if source_spec.get(level) is None:
                continue
            if level not in spec:
                self.initialize(spec, level)
            indexes = sorted(
              [k for k in source_spec[level] if str(k).isdigit()])
            # Apply "all" to all indexes
            if "all" in source_spec.get(level, {}):
                all_indexes = sorted(list(
                  set(indexes + [k for k in spec[level] if str(k).isdigit()])))
                for index in all_indexes:
                    if index not in spec[level]:
                        self.initialize(spec[level], index)
                    self.process_level(spec[level][index],
                      source_spec[level]["all"], indexed_levels.get(level, {}),
                      path=path + [level, index])
            # Loop over specific indexes
            for index in indexes:
                # Add dict in which to store lower levels
                if index not in spec[level]:
                    self.initialize(spec[level], index)
                self.process_level(spec[level][index],
                  source_spec[level].get(index, {}),
                  indexed_levels.get(level, {}), path=path + [level, index])