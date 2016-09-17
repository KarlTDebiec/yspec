#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.PresetsPlugin.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Adds preset argument groups to a nascent spec
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("yspec.plugins")
    import yspec.plugins
from . import YSpecPlugin
################################### CLASSES ###################################
class PresetsPlugin(YSpecPlugin):
    """
    Adds preset argument groups to a nascent spec

    Attributes
      name (str): Name of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
      available_presets (dict): Available presets; outermost keys are
        the preset names, while the values are the arguments associated
        with each preset
    """
    name = "presets"
    description = """Add selected group(s) of 'preset' arguments to nascent
      spec."""

    @classmethod
    def construct_argparser(class_, parser, **kwargs):
        """
        Adds arguments to a nascent argument parser

        Arguments:
          parser (ArgumentParser): Parser to which arguments will be
            added
          kwargs (dict): Additional keyword arguments

        Returns:
          ArgumentParser: Argument parser
        """

        super(PresetsPlugin, class_).construct_argparser(parser=parser,
          **kwargs)

        arg_group = parser.add_argument_group("Settings for {0} plugin".format(
          class_.name))
#        arg_group.add_argument(
#          "-available-presets",
#          dest     = "available_presets",
#          type     = str,
#          help     = """input file from which to load available presets (yaml
#                     format)""")
        arg_group.add_argument(
          "-presets",
          dest     = "selected_presets",
          type     = str,
          nargs    = "*",
          metavar  = "PRESET",
          help     = "selected presets to apply to entire spec")

        return parser

    def __init__(self, indexed_levels=None, available_presets=None,**kwargs):
        """
        """

        if indexed_levels is not None:
            self.indexed_levels = indexed_levels
        else:
            self.indexed_levels = {}
        if available_presets is not None:
            self.available_presets = available_presets
        else:
            self.available_presets = {}

    def __call__(self, spec, source_spec=None, **kwargs):
        """
        Adds preset argument groups to a nascent spec

        Arguments:
          spec (CommentedMap): Nascent spec
          source_spec (dict): Source spec to use to determine where
            defaults should be added

        Returns:
          CommentedMap: Updated spec including preset arguments
        """
        selected_presets = kwargs.get("selected_presets", [])

        self.process_level(spec, source_spec, self.indexed_levels,
          self.available_presets, selected_presets=selected_presets)
        return spec

    def process_level(self, spec, source_spec, indexed_levels,
        available_presets, selected_presets=None, path=None):
        """
        Adds selected preset arguments to one level of spec hierarchy

        Arguments:
          spec (CommentedMap): Nascent spec at current level
          source_spec (dict): Source spec at current level
          indexed_levels (dict): Indexed levels below current level
          available_presets (dict): Available presets within current
            level
          selected_presets (list): Presets selected above current level
          path (list): List of keys leading to this level
        """
        import six

        # Process arguments
        if available_presets is None:
            return
        if indexed_levels is None:
            indexed_levels = {}
        if selected_presets is None:
            selected_presets = []
        else:
            selected_presets = selected_presets[:]
        if source_spec is None:
            source_spec = {}
        if path is None:
            # At base level of file, presets passed at command line override
            # presets read from file
            path = []
            source_spec_presets = source_spec["presets"]
            if isinstance(source_spec_presets, six.string_types):
                source_spec_presets = [source_spec_presets]
            temp = source_spec_presets
            for preset in selected_presets:
                if preset in temp:
                    temp.remove(preset)
                temp += [preset]
            selected_presets = temp
        elif "presets" in source_spec:
            # At subsequent levels, presets read at this level override presets
            # inherited from levels above
            source_spec_presets = source_spec["presets"]
            if isinstance(source_spec_presets, six.string_types):
                source_spec_presets = [source_spec_presets]
            for preset in source_spec_presets:
                if preset in selected_presets:
                    selected_presets.remove(preset)
                selected_presets += [preset]

        # Loop over presets that are currently selected
        for selected_preset in selected_presets:
            if selected_preset not in available_presets:
                continue

            # Loop over preset argument keys and values at this level
            for preset_key, preset_val in [(k, v)
                    for k, v in available_presets[selected_preset].items()
                    if not k.startswith("_")]:
                # This level is indexed; loop over indexes as well
                if preset_key in indexed_levels:
                    # Make new dict of available_presets including only
                    # those applicable to the next level
                    if preset_key not in spec:
                        continue
                    for index in sorted([k for k in spec[preset_key]
                            if str(k).isdigit()]):
                        # Make new dict of available_presets including only
                        # those applicable to the next level
                        level_available_presets = {k: v[preset_key]
                          for k, v in available_presets.items()
                          if preset_key in v}
                        self.process_level(
                          spec[preset_key][index],
                          source_spec.get(preset_key, {}).get(index, {}),
                          indexed_levels.get(preset_key, {}),
                          level_available_presets,
                          selected_presets,
                          path=path+[preset_key, index])
                # This level is not indexed
                else:
                    # preset_val is a dict; recurse
                    if isinstance(preset_val, dict):
                        # Make new dict of available_presets including only
                        # those applicable to the next level
                        level_available_presets = {k: v[preset_key]
                          for k, v in available_presets.items()
                          if preset_key in v}
                        if preset_key not in spec:
                            self.initialize(spec, preset_key,
                              comment="{0}:{1}".format(self.name,
                              selected_preset))
                        self.process_level(
                          spec[preset_key],
                          source_spec.get(preset_key, {}),
                          indexed_levels.get(preset_key, {}),
                          level_available_presets,
                          selected_presets,
                          path=path+[preset_key])
                    # preset_val is singular; store and continue loop
                    else:
                        self.set(spec, preset_key, preset_val,
                          comment="{0}:{1}".format(self.name, selected_preset))
