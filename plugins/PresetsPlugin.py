#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.plugins.PresetsPlugin.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Adds preset argument groups to a nascent spec
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

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
      description (str): Description of this plugin
      indexed_levels (dict): Levels of spec hierarchy that include an
        additional layer of indexes below them
      available_presets (dict): Available presets; outermost keys are
        the preset names, while the values are the arguments associated
        with each preset
    """
    name = "presets"
    description = """adds selected 'preset' arguments to nascent spec"""

    @classmethod
    def add_arguments(cls, parser, **kwargs):
        """
        Adds arguments to a nascent argument parser

        Arguments:
          parser (ArgumentParser): Parser to which arguments will be
            added
          kwargs (dict): Additional keyword arguments

        Returns:
          ArgumentParser: Argument parser
        """
        from collections import OrderedDict
        from textwrap import wrap

        # Arguments unique to this plugin
        arg_group = parser.add_argument_group(
          "arguments for {0} plugin".format(cls.name))
        cls.add_argument(arg_group, "-presets", dest="selected_presets",
          type=str, nargs="+", metavar="PRESET",
          help="selected presets to apply to entire spec")

        # Format preset help text and extension pattern
        available_presets = cls.initialize_available_presets(**kwargs)
        if len(available_presets) == 0:
            description = "no presets available\n"
        else:
            description = "available presets:\n"
            base_presets = OrderedDict(sorted(
              [(k, v) for k, v in available_presets.items() if
                  "_extends" not in v]))
            for preset_name, preset in base_presets.items():
                extensions = sorted(
                  [(k, v) for k, v in available_presets.items() if
                      v.get("_extends") == preset_name])
                symbol = "│" if len(extensions) > 0 else " "
                if "_help" in preset:
                    wrapped = wrap(preset["_help"], 54)
                    if len(preset_name) > 20:
                        description += "  {0}\n".format(preset_name)
                        description += "  {0} {1:19}".format(symbol, " ")
                    else:
                        description += "  {0:18s}".format(preset_name)
                    description += "{0}\n".format(wrapped.pop(0))
                    for line in wrapped:
                        description += "   {0} {1:19}{2}\n".format(symbol, " ",
                          line)
                else:
                    description += "  {0}\n".format(preset_name)
                for i, (extension_name, extension) in enumerate(extensions, 1):
                    symbol = "└" if i == len(extensions) else "├"
                    if "_help" in extension:
                        wrapped = wrap(extension["_help"], 51)
                        if len(extension_name) > 16:
                            description += "   {0} {1}\n".format(symbol,
                              extension_name)
                            symbol = "│" if i != len(extensions) else " "
                            description += "   {0} {1:15}".format(symbol, " ")
                        else:
                            description += "   {0} {1:15}".format(symbol,
                              extension_name)
                        description += "{0}\n".format(wrapped.pop(0))
                        symbol = "│" if i != len(extensions) else " "
                        for line in wrapped:
                            description += "   {0} {1:19}{2}\n".format(symbol,
                              " ", line)
                    else:
                        description += " {0} {1}\n".format(symbol,
                          extension_name)
        arg_group.description = description

        # Arguments inherited from superclass
        super(PresetsPlugin, cls).add_arguments(parser=parser, **kwargs)

        return parser

    @classmethod
    def initialize_available_presets(cls, **kwargs):
        """
        Initializes available presets, carrying out inheritance and
        extension

        Arguments:
          constructor (YSpecConstructor): Constructor for which parser
            is being built

        returns:
           dict: Available presets, after inheritance and extension
        """
        from inspect import getmro
        from .. import merge_dicts

        constructor = kwargs.get("constructor", None)
        available_presets = cls.get_config("available_presets", **kwargs)
        if available_presets is None:
            return {}

        # Cannot figure out how to use super() here
        if isinstance(constructor, type):
            mro = getmro(constructor)
        else:
            mro = getmro(type(constructor))
        if len(mro) >= 2:
            super_presets = cls.initialize_available_presets(
              constructor=mro[1])
        else:
            super_presets = {}

        for name, preset in available_presets.items():
            if "_inherits" in preset:
                parent_name = preset["_inherits"]
                if parent_name in super_presets:
                    available_presets[name] = merge_dicts(
                      super_presets[parent_name], preset)

        for name, preset in available_presets.items():
            if "_extends" in preset:
                parent_name = preset["_extends"]
                if parent_name in available_presets:
                    available_presets[name] = merge_dicts(
                      available_presets[parent_name], preset)

        return available_presets

    def __init__(self, **kwargs):
        """
        """
        self.indexed_levels = self.get_config("indexed_levels",
          attr_of_constructor=True, **kwargs)
        self.available_presets = self.initialize_available_presets(**kwargs)

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
            source_spec_presets = source_spec.get("presets", [])
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
            for preset_key, preset_val in [(k, v) for k, v in
                available_presets[selected_preset].items() if
                not k.startswith("_")]:
                # This level is indexed; loop over indexes as well
                if preset_key in indexed_levels:
                    # Make new dict of available_presets including only
                    # those applicable to the next level
                    if preset_key not in spec:
                        continue
                    for index in sorted(
                      [k for k in spec[preset_key] if str(k).isdigit()]):
                        # Make new dict of available_presets including only
                        # those applicable to the next level
                        level_available_presets = {k: v[preset_key] for k, v in
                            available_presets.items() if preset_key in v}
                        self.process_level(spec[preset_key][index],
                          source_spec.get(preset_key, {}).get(index, {}),
                          indexed_levels.get(preset_key, {}),
                          level_available_presets, selected_presets,
                          path=path + [preset_key, index])
                # This level is not indexed
                else:
                    # preset_val is a dict; recurse
                    if isinstance(preset_val, dict):
                        # Make new dict of available_presets including only
                        # those applicable to the next level
                        level_available_presets = {k: v[preset_key] for k, v in
                            available_presets.items() if preset_key in v}
                        if preset_key not in spec:
                            self.initialize(spec, preset_key,
                              comment="{0}:{1}".format(self.name,
                                selected_preset))
                        self.process_level(spec[preset_key],
                          source_spec.get(preset_key, {}),
                          indexed_levels.get(preset_key, {}),
                          level_available_presets, selected_presets,
                          path=path + [preset_key])
                    # preset_val is singular; store and continue loop
                    else:
                        self.set(spec, preset_key, preset_val,
                          comment="{0}:{1}".format(self.name, selected_preset))