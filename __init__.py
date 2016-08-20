# -*- coding: utf-8 -*-
#   yspec.__init__.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
General functions.

.. todo:
  - Check InterSphinx link in wrapprint
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
################################## FUNCTIONS ##################################
def wrapprint(text, width=80, subsequent_indent="  ", **kwargs):
    """
    Prints wrapped text.

    Arguments:
      text (str): Text to wrap
      width (int): Width of formatted text
      subsequent_indent (str): Text with which to prepend lines after
        the first
      kwargs (dict): Additional keyword arguments passed to
        :func:`TextWrapper`
    """
    import re
    from textwrap import TextWrapper

    tw = TextWrapper(width=width, subsequent_indent=subsequent_indent,
           **kwargs)
    print(tw.fill(re.sub(r"\s+", " ", text)))

def sformat(text, **kwargs):
    """
    Formats whitespace in text.

    Arguments:
      text (str): Text to format
    Returns:
      str: *text* with all whitespace replaced with single spaces
    """
    import re

    return(re.sub(r"\s+", " ", text))

def get_yaml(input):
    """
    Generates data structure from yaml input. 

    Arguments:
      input (str, dict): yaml input; if str, tests whether or not it is
        a path to a yaml file. If it is, the file is loaded using yaml;
        if it is not a file, the string itself is loaded using yaml. If
        dict, returned without modification

    Returns:
      dict: Data structure specified by input

    Warns:
      UserWarning: Loaded data structure is a string; occurs if input
        file is a path to a yaml file that is not found

    Raises:
      TypeError: Input is not str or dict
    """
    from os.path import isfile
    from warnings import warn
    import yaml
    import six

    if six.PY2:
        open_yaml = file
    else:
        open_yaml = open

    if isinstance(input, dict):
        return input
    elif isinstance(input, six.string_types):
        if isfile(input):
            with open_yaml(input, "r") as infile:
                return yaml.load(infile)
        else:
            output = yaml.load(input)
            if isinstance(output, str):
                warn("""yspec.get_yaml() has loaded input '{0}' as a string
                  rather than a dictionary or other data structure; if input
                  was intended as an infile it was not
                  found.)""".format(input))
            return output
    elif input is None:
        warn("""yspec.get_yaml() has been asked to load input 'None', and will
          return an empty dictionary.""")
        return {}
    else:
        raise TypeError("""yspec.get_yaml() does not support input of type {0};
          input may be a string path to a yaml file, a yaml-format string, or a
          dictionary.""".format(input.__class__.__name__))
