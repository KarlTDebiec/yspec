#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.ManualPlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Copies arguments to nascent spec from source spec
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("yspec.plugins")
    import yspec.plugins
from . import YSpecPlugin
################################### CLASSES ###################################
class ManualPlugin(YSpecPlugin):
    """
    Copies arguments to nascent spec from source spec

    Attributes
      name (str): Name of this plugin
      description (str): Description of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
    """
    name = "manual"
    description = """copies arguments to nascent spec from source spec"""

    def __init__(self, **kwargs):
        """
        """
        self.indexed_levels = self.get_config("indexed_levels",
          attr_of_constructor=True, **kwargs)

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Adds manually-set arguments to a nascent spec.

        Arguments:
          spec (CommentedMap): Nascent spec
          source_spec (dict): Source spec used as source of manual
            arguments

        Returns:
          CommentedMap: Updated spec including maually-set arguments
        """
        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels)
        return spec

    def process_level(self, spec, source_spec, indexed_levels, path=None):
        """
        Adds manually-set arguments to one level of spec hierarchy

        Arguments:
          spec (CommentedMap): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels within current level
          path (list): List of keys leading to this level
        """

        # Process arguments
        if source_spec is None:
            return
        if indexed_levels is None:
            indexed_levels = {}
        if path is None:
            path = []

        # Loop over source argument keys and values at this level
        for source_key, source_val in source_spec.items():

            # This level is indexed; loop over indexes as well
            if source_key in indexed_levels:
                if source_spec.get(source_key) is None:
                    # Not clear if this is the appropriate behavior here or not
                    continue
                # Apply arguments from "all" first
                if "all" in source_spec.get(source_key, {}):
                    for index in sorted([k for k in spec[source_key]
                                 if str(k).isdigit()]):
                        self.process_level(
                          spec[source_key][index],
                          source_spec[source_key]["all"],
                          indexed_levels.get(source_key, {}),
                          path=path+[source_key, index])
                # Apply index-specific arguments second
                for index in sorted([k for k in spec[source_key]
                             if str(k).isdigit()]):
                    self.process_level(
                      spec[source_key][index],
                      source_spec.get(source_key, {}).get(index, {}),
                      indexed_levels.get(source_key, {}),
                      path=path+[source_key, index])
            # This level is not indexed
            else:
                # source_val is a dict; recurse
                if isinstance(source_val, dict):
                    if source_key not in spec or spec[source_key] is None:
                        self.initialize(spec, source_key)
                    self.process_level(
                      spec[source_key],
                      source_spec.get(source_key, {}),
                      indexed_levels.get(source_key, {}),
                      path=path+[source_key])
                # source_val is singular; store and continue loop
                else:
                    self.set(spec, source_key, source_val)
