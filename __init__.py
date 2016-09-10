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
  - wrapprint
    - Check InterSphinx link
  - format_spec
    - Allow cutoff at 80 columns (or otherwise) with ...
    - Colored output based on source
  - yaml_load
    - Double-check that warning/exception text wraps correctly
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
import re
import ruamel.yaml as yaml
import six
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
    from textwrap import TextWrapper

    tw = TextWrapper(width=width, subsequent_indent=subsequent_indent,
           **kwargs)
    print(tw.fill(re.sub(r"\s+", " ", text)))

def strfmt(text, width=None, subsequent_indent="  ", **kwargs):
    """
    Formats whitespace in text.

    Arguments:
      text (str): Text to format
      width (int): Width of formatted text
      subsequent_indent (str): Text with which to prepend lines after
        the first
      kwargs (dict): Additional keyword arguments passed to
        :func:`TextWrapper`
    Returns:
      str: *text* with whitespace formatted as directed
    """
    from textwrap import TextWrapper

    if width is None:
        return(re.sub(r"\s+", " ", text).strip())
    else:
        tw = TextWrapper(width=width, subsequent_indent=subsequent_indent,
               **kwargs)
        return(tw.fill(re.sub(r"\s+", " ", text).strip()))

def yaml_load(input_):
    """
    Generates data structure from yaml input. 

    Arguments:
      input_ (str, dict): yaml input; if str, tests whether or not it is
        a path to a yaml file. If it is, the file is loaded using yaml;
        if it is not a file, the string itself is loaded using yaml. If
        dict, returned without modification

    Returns:
      dict: Data structure specified by *input_*

    Warns:
      UserWarning: Loaded data structure is a string; occurs if input
        file is a path to a yaml file that is not found

    Raises:
      TypeError: Input is not str or dict
    """
    from os.path import isfile
    from warnings import warn

    if six.PY2:
        open_yaml = file
    else:
        open_yaml = open

    if isinstance(input_, six.string_types):
        if isfile(input_):
            with open_yaml(input_, "r") as infile:
                return yaml.load(infile, Loader=yaml.RoundTripLoader)
        else:
            output = yaml.load(input_, Loader=yaml.RoundTripLoader)
            if isinstance(output, six.string_types):
                warn("""yspec.yaml_load() has loaded input '{0}' as a string
                  rather than a dictionary or other data structure; if input
                  was intended as an infile it was not
                  found.)""".format(input_))
            return output
    elif isinstance(input_, dict):
        return input_
    elif input_ is None:
        warn("""yspec.yaml_load() has been asked to load input 'None', and will
          return an empty dictionary.""")
        return {}
    else:
        raise TypeError("""yspec.yaml_load() does not support input of type
          '{0}'; input may be a string containing the path to a yaml file, a
          string containing yaml-formatted data, or a
          dict.""".format(input.__class__.__name__))

def yaml_dump(spec, **kwargs):
    """
    """
    dump_kw = dict(
      Dumper           = yaml.RoundTripDumper,
      block_seq_indent = 2,
      indent           = 4)
    dump_kw.update(kwargs)
    return yaml.dump(spec, **dump_kw).strip()
