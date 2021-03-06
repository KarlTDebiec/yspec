#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.DefaultsPlugin.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Adds default arguments to a nascent spec
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

if __name__ == "__main__":
    __package__ = str("yspec.plugins")
    import yspec.plugins
from . import YSpecPlugin


################################### CLASSES ###################################
class DefaultsPlugin(YSpecPlugin):
    """
    Adds default arguments to a nascent spec

    Attributes
      name (str): Name of this plugin
      description (str): Description of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
      defaults (dict): Default arguments
    """
    name = "defaults"
    description = """adds default arguments to nascent spec"""

    def __init__(self, **kwargs):
        """
        """
        self.indexed_levels = self.get_config("indexed_levels",
          attr_of_constructor=True, **kwargs)
        self.defaults = self.get_config("defaults", **kwargs)

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Adds default arguments to nascent spec

        Arguments:
          spec (CommentedMap): Nascent spec
          source_spec (dict): Source spec to use to determine where
            defaults should be added

        Returns:
          CommentedMap: Updated spec including default arguments
        """
        if source_spec is not None:
            self.process_level(spec, source_spec, self.indexed_levels,
              self.defaults)
        return spec

    def process_level(self, spec, source_spec, indexed_levels, defaults):
        """
        Adds default arguments to one level of spec hierarchy

        Arguments:
          spec (CommentedMap): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels within current level
          defaults (dict): Defaults within current level
        """

        # Process arguments
        if defaults is None:
            return
        if indexed_levels is None:
            indexed_levels = {}
        if source_spec is None:
            source_spec = {}

        # Loop over default argument keys and values at this level
        for default_key, default_val in defaults.items():

            # This level is indexed; loop over indexes as well
            if default_key in indexed_levels:
                if default_key not in spec:
                    continue
                indexes = sorted(
                  [k for k in spec[default_key] if str(k).isdigit()])
                for index in indexes:
                    self.process_level(spec[default_key][index],
                      source_spec.get(default_key, {}).get(index, {}),
                      indexed_levels.get(default_key, {}), default_val)
            # This level is not indexed
            else:
                # default_val is a dict; recurse
                if isinstance(default_val, dict):
                    if default_key not in spec:
                        self.initialize(spec, default_key)
                    self.process_level(spec[default_key],
                      source_spec.get(default_key, {}),
                      indexed_levels.get(default_key, {}), default_val)
                # default_val is singular; store and continue loop
                else:
                    self.set(spec, default_key, default_val)