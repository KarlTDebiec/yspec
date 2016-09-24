#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.YSpecConstructor.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Constructs yaml-format specification
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("yspec")
    import yspec
from . import YSpecCLTool
################################### CLASSES ###################################
class YSpecConstructor(YSpecCLTool):
    """
    Constructs yaml-format specification
    """
    from collections import OrderedDict
    from .plugins.InitializePlugin import InitializePlugin
    from .plugins.DefaultsPlugin import DefaultsPlugin
    from .plugins.PresetsPlugin import PresetsPlugin
    from .plugins.ManualPlugin import ManualPlugin
    from .plugins.SortPlugin import SortPlugin
    available_plugins = OrderedDict([
      ("initialize", InitializePlugin),
      ("defaults", DefaultsPlugin),
      ("presets", PresetsPlugin),
      ("manual", ManualPlugin),
      ("sort", SortPlugin)])
    default_plugins = ["initialize", "defaults", "presets", "manual", "sort"]
    indexed_levels = """"""
    plugin_config = dict()

    @classmethod
    def construct_argparser(class_, **kwargs):
        """
        Adds arguments to a nascent argument parser

        Arguments:
          kwargs (dict): Additional keyword arguments

        Returns:
          ArgumentParser: Argument parser or subparser
        """

        # Process arguments
        parser = class_.get_argparser(**kwargs)
        if parser.get_default("class_") is None:
            parser.set_defaults(class_=class_)

        verbosity = class_.add_mutually_exclusive_argument_group(parser,
          "verbosity")
        class_.add_argument(verbosity,
          "-v", "--verbose",
          action   = "count",
          default  = 1,
          help     = "enable verbose output, may be specified more than once")
        class_.add_argument(verbosity,
          "-q", "--quiet",
          action   = "store_const",
          const    = 0,
          default  = 1,
          dest     = "verbose",
          help     = "disable verbose output")
        class_.add_argument(parser,
          "-d", "--debug",
          action   = "count",
          default  = 1,
          help     = "enable debug output, may be specified more than once")

        if len(class_.available_plugins) > 0:
            if (hasattr(class_, "default_plugins")
            and len(class_.default_plugins) > 0):
                parser.description += \
                  "\ndefault plugin order:\n  {0}\n\n".format(
                  " → ".join( class_.default_plugins))
            parser.description += "available plugins:\n"
            for name, plugin in class_.available_plugins.items():
                plugin.add_arguments(parser, constructor=class_)

        class_.add_argument(parser,
          "-spec",
          required = True,
          dest     = "source_spec",
          metavar  = "SPEC",
          type     = str,
          help     = "input file from which to load source spec")
        parser.set_defaults(class_=class_)

        return parser

    def __init__(self, source_spec=None, plugins=None, **kwargs):
        """
        Arguments:
          source_spec (str): Path to source spec infile
          plugins (list, optional): Sequence of plugins with which to
            prepare spec
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments
        """
        from ruamel.yaml.comments import CommentedMap
        from . import yaml_load, yaml_dump

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        self.source_spec = yaml_load(source_spec)
        if plugins is None:
            self.plugins = self.default_plugins

        # Prepare spec
        self.spec = CommentedMap()
        for plugin_name in self.plugins:
            plugin = self.available_plugins[plugin_name](constructor=self,
              **kwargs)
            self.spec = plugin(self.spec, self.source_spec, **kwargs)
            # Output intermediate spec
            if verbose >= 3:
                print("\nSpec after running {0} plugin:".format(plugin_name))
                print(yaml_dump(self.spec))

        # Output spec
        if verbose >= 2:
            print("\nFinal spec:")
            print(yaml_dump(self.spec))

    @classmethod
    def main(class_):
        """
        """
        # Prepare argument parser
        parser = class_.construct_argparser()

        # Parse arguments
        kwargs = vars(parser.parse_args())
        kwargs.pop("class_")(**kwargs)

#################################### MAIN #####################################
if __name__ == "__main__":
    YSpecConstructor.main()
