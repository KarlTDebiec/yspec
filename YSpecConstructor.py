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
import ruamel.yaml as yaml
################################### CLASSES ###################################
class YSpecConstructor(object):
    """
    """
    from .plugins.InitializePlugin import InitializePlugin
    from .plugins.DefaultsPlugin import DefaultsPlugin
    from .plugins.PresetsPlugin import PresetsPlugin
    from .plugins.ManualPlugin import ManualPlugin
    available_plugins = dict(
      initialize = InitializePlugin,
      defaults   = DefaultsPlugin,
      presets    = PresetsPlugin,
      manual     = ManualPlugin)
    indexed_levels = None
    plugin_config = None

    def __init__(self, source_spec=None, **kwargs):
        """
        """
        from yspec import yaml_load, yaml_dump

        plugins = ["initialize", "defaults", "presets", "manual"]
        self.source_spec = yaml_load(source_spec)
        spec = yaml.comments.CommentedMap()
        for plugin_name in plugins:
            plugin = self.available_plugins[plugin_name](
              indexed_levels=yaml_load(self.indexed_levels),
              **yaml_load(self.plugin_config.get(plugin_name, {})))
            spec = plugin(spec, self.source_spec)
            with open ("test_{0}.yml".format(plugin_name), "w") as outfile:
                outfile.write(yaml_dump(spec))
        self.spec = spec

    @classmethod
    def main(class_):
        """
        """
        import argparse

        # Prepare argument parser
        parser = argparse.ArgumentParser(
          description = __doc__)
        parser.add_argument(
          "-spec",
          required = True,
          dest     = "source_spec",
          metavar  = "SPEC",
          type     = str,
          help     = "input file from which to load specification")
        parser.set_defaults(class_=class_)

        # Parse arguments
        kwargs = vars(parser.parse_args())
        kwargs.pop("class_")(**kwargs)

#################################### MAIN #####################################
if __name__ == "__main__":
    YSpecConstructor.main()
