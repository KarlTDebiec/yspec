#!/usr/bin/python
# -*- coding: utf-8 -*-
#   TestYSpecConstructor.py
#
#   Copyright (C) 2015-2017 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Test constructor
"""
################################### MODULES ###################################
from __future__ import (absolute_import, division, print_function,
    unicode_literals)

from yspec.YSpecConstructor import YSpecConstructor


################################### CLASSES ###################################
class TestYSpecConstructor(YSpecConstructor):
    """
    """
    from yspec.plugins.InitializePlugin import InitializePlugin
    from yspec.plugins.DefaultsPlugin import DefaultsPlugin
    from yspec.plugins.PresetsPlugin import PresetsPlugin
    from yspec.plugins.ManualPlugin import ManualPlugin
    from yspec.plugins.SortPlugin import SortPlugin

    available_plugins = dict(initialize=InitializePlugin,
        defaults=DefaultsPlugin, presets=PresetsPlugin, manual=ManualPlugin,
        sort=SortPlugin)
    default_plugins = ["initialize", "defaults", "presets", "manual", "sort"]
    indexed_levels = """
      level_1:
          level_2:
              level_3:"""
    plugin_config = dict(defaults="""
        defaults:
          default_0.0: default_0.0_value
          level_1:
            default_1.1:
              default_1.1.1: default_1.1.1_value
            level_2:
              default_2.1: default_2.1_value
              level_3:
                default_3.1: default_3.1_value""", presets="""
        available_presets:
          preset_1:
            _class: preset_class_1
            _help: Preset #1
            level_1:
              preset_1_1.1:
                preset_1_1.1.1: preset_1_1.1.1_value
              level_2:
                preset_1_2.1: preset_1_2.1_value
                level_3:
                  preset_1_3.1: preset_1_3.1_value
          preset_2:
            _class: preset_class_1
            _help: Preset #2
            level_1:
              preset_2_1.1:
                preset_2_1.1.1: preset_2_1.1.1_value
              level_2:
                preset_2_2.1: preset_2_2.1_value
                level_3:
                  preset_2_3.1: preset_2_3.1_value""")


#################################### MAIN #####################################
if __name__ == "__main__":
    TestYSpecConstructor.main()
