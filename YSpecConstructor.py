#!/usr/bin/python
# -*- coding: utf-8 -*-
#   yspec.YSpecConstructor.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Constructs yaml-format specification
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

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
    available_plugins = OrderedDict(
        [("initialize", InitializePlugin), ("defaults", DefaultsPlugin),
            ("presets", PresetsPlugin), ("manual", ManualPlugin),
            ("sort", SortPlugin)])
    default_plugins = ["initialize", "defaults", "presets", "manual", "sort"]
    indexed_levels = """"""
    plugin_config = dict()

    @classmethod
    def construct_argparser(cls, **kwargs):
        """
        Adds arguments to a nascent argument parser

        Arguments:
          kwargs (dict): Additional keyword arguments

        Returns:
          ArgumentParser: Argument parser or subparser
        """

        # Process arguments
        parser = cls.get_argparser(**kwargs)
        if parser.get_default("cls") is None:
            parser.set_defaults(cls=cls)

        verbosity = cls.add_mutually_exclusive_argument_group(parser,
            "verbosity")
        cls.add_argument(verbosity, "-v", "--verbose", action="count",
            default=1,
            help="enable verbose output, may be specified more than once")
        cls.add_argument(verbosity, "-q", "--quiet", action="store_const",
            const=0, default=1, dest="verbose", help="disable verbose output")
        cls.add_argument(parser, "-d", "--debug", action="count", default=1,
            help="enable debug output, may be specified more than once")

        if len(cls.available_plugins) > 0:
            if (hasattr(cls, "default_plugins") and len(
                cls.default_plugins) > 0):
                parser.description += "\ndefault plugin order:\n  {" \
                                      "0}\n\n".format(
                    " → ".join(cls.default_plugins))
            parser.description += "available plugins:\n"
            for name, plugin in cls.available_plugins.items():
                plugin.add_arguments(parser, constructor=cls)

        cls.add_argument(parser, "-spec", required=True, dest="source_spec",
            metavar="SPEC", type=str,
            help="input file from which to load source spec")
        parser.set_defaults(cls=cls)

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
    def main(cls):
        """
        """
        # Prepare argument parser
        parser = cls.construct_argparser()

        # Parse arguments
        kwargs = vars(parser.parse_args())
        kwargs.pop("cls")(**kwargs)


#################################### MAIN #####################################
if __name__ == "__main__":
    YSpecConstructor.main()
