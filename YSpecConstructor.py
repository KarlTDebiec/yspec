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
################################### CLASSES ###################################
class YSpecConstructor(object):
    """
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

    def __init__(self, source_spec=None, plugins=None, **kwargs):
        """
        Arguments:
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
        import argparse

        # Prepare argument parser
        parser = argparse.ArgumentParser(
          formatter_class = argparse.RawDescriptionHelpFormatter,
          description     = __doc__,
          epilog          = "")
        verbosity = parser.add_mutually_exclusive_group()
        verbosity.add_argument(
          "-v",
          "--verbose",
          action   = "count",
          default  = 1,
          help     = "enable verbose output, may be specified more than once")
        verbosity.add_argument(
          "-q",
          "--quiet",
          action   = "store_const",
          const    = 0,
          default  = 1,
          dest     = "verbose",
          help     = "disable verbose output")

        parser.add_argument(
          "-d",
          "--debug",
          action   = "count",
          default  = 0,
          help     = "enable debug output, may be specified more than once")

        if len(class_.available_plugins) > 0:
            parser.description += "\ndefault plugin order:\n  {0}\n\n".format(
              " → ".join(class_.available_plugins.keys()))
            parser.description += "available plugins:\n"
            for name, plugin in class_.available_plugins.items():
                plugin.construct_argparser(parser, constructor=class_)

        parser.add_argument(
          "-spec",
          required = True,
          dest     = "source_spec",
          metavar  = "SPEC",
          type     = str,
          help     = "input file from which to load source spec")
        parser.set_defaults(class_=class_)

        # Parse arguments
        kwargs = vars(parser.parse_args())
        kwargs.pop("class_")(**kwargs)

#################################### MAIN #####################################
if __name__ == "__main__":
    YSpecConstructor.main()
