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
    - Where to store source spec?
    - Where to store list of plugins?
    - Formatted printing option that returns list of strings
    """

    def __init__(self, source_spec=None, **kwargs):
        """
        """
        from . import get_yaml, format_spec
        self.source_spec = get_yaml(source_spec)
        print(format_spec(self.source_spec))
        # Read yaml file?
        # Should be possible to set defaults and presets from string or file
        # if os.path.isfile(defaults):
        #   self.available_defaults = pyyaml.read(defaults)
        # elif:
        #   self.available_defaults = defaults
        # Call construct with kwargs

    def construct(self, kwargs):
        """
        """
        pass
        # Each plugin must be passed this object
        #   (Almost) all will want to read nascent and source specs
        #   Defaults and Presets also need to access attributes of the
        #   constructor
        # Should not need to know about other plugins

#################################### MAIN #####################################
def main():
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

    # Source spec infile
    # Plugins
    # Arguments from plugins
    #   Defaults infile
    #   Presets infile
    parser.set_defaults(class_=YSpecConstructor)
    kwargs = vars(parser.parse_args())
    kwargs.pop("class_")(**kwargs)

if __name__ == "__main__":
    main()
