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
    Prints wrapped text

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
    Formats whitespace in text

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

def merge_dicts(dict_1, dict_2):
    """
    Recursively merges two dictionaries

    Arguments:
      dict_1 (dict): First dictionary
      dict_2 (dict): Second dictionary; values for keys shared by both
        dictionaries are drawn from dict_2

    Returns:
      dict: Merged dictionary

    Raises:
      AttributeError: Either dict_1 or dict_2 lacks 'keys' function
    """

    def merge(dict_1, dict_2):
        """
        Generator used to recursively merge two dictionaries

        Arguments:
          dict_1 (dict): First dictionary
          dict_2 (dict): Second dictionary; values for keys shared by
            both dictionaries are drawn from dict_2

        Yields:
          tuple: Merged (key, value) pair
        """
        for key in set(dict_1.keys()).union(dict_2.keys()):
            if key in dict_1 and key in dict_2:
                if (isinstance(dict_1[key], dict)
                and isinstance(dict_2[key], dict)):
                    yield (key, dict(merge(dict_1[key], dict_2[key])))
                else:
                    yield (key, dict_2[key])
            elif key in dict_1:
                yield (key, dict_1[key])
            else:
                yield (key, dict_2[key])

    if not isinstance(dict_1, dict) or not isinstance(dict_2, dict):
        raise Exception(strfmt("""Function yspec.merge_dicts() requires
          arguments 'dict_1' and 'dict_2' to be dictionaries; arguments
          of types '{0}' and '{1}' provided""".format(
          dict_1.__class__.__name__, dict_2.__class__.__name__)))

    return dict(merge(dict_1, dict_2))

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

def yaml_dump(spec, colored=True, **kwargs):
    """
    """
    dump_kw = dict(
      Dumper           = yaml.RoundTripDumper,
      block_seq_indent = 2,
      indent           = 4)
    dump_kw.update(kwargs)
    output = yaml.dump(spec, **dump_kw).strip()
    if colored:
        import re
        from termcolor import colored

        colored_output = ""
        available_colors = ["red", "green", "yellow", "blue", "magenta", "cyan"]
        selected_colors = {}
        for line in output.split("\n"):
            re_comment = re.compile(
              "^(?P<line>.*)#[\s]*?(?P<plugin>[^\s:]+):?(?P<subplugin>[^\s]+)?$")
            match = re.match(re_comment, line)
            if match:
                plugin    = match.groupdict()["plugin"]
                subplugin = match.groupdict()["subplugin"]
                if plugin not in selected_colors:
                    selected_colors[plugin] = available_colors.pop(0)
                if subplugin is not None:
                    pass
                color = selected_colors[plugin]
                colored_output += colored(line, color) + "\n"
            else:
                colored_output += colored(line, "white") + "\n"
        return colored_output
    else:
        return output
################################### CLASSES ###################################
class YSpecCLTool(object):
    """
    Base class for YSpec command line tools; includes convenience functions
    """

    @staticmethod
    def add_argument(parser, *args, **kwargs):
        """
        Adds an argument to a nascent argument parser; if an argument
        with the same name is not already present

        Arguments:
          parser (ArgumentParser): Nascent argument parser
        """
        import argparse

        try:
            parser.add_argument(*args, **kwargs)
        except argparse.ArgumentError:
            pass

    @staticmethod
    def add_mutually_exclusive_argument_group(parser, name):
        """
        Adds a mutually exclusive argument group to a nascent argument
        parser, or returns pre-existing group

        Unfortunately; manually maintaining a dictionary of
        mutually-exclusive argument groups appears to be the best way to
        avoid the failure that results when arguments with the same name
        are added to multiple mutually-exclusive groups. When an
        argument is added to a mutually-exclusive group, no checking is
        performed to ensure that an argument with the same name is not
        present in another mutually-exclusive groups. The conflict is
        not caught until parse_args() is called, making it impossible to
        use try/except to add arguments only if they are not already
        present in the parser, as may be done for arguments that are not
        part of a mutually-exclusive group. Furthermore,
        add_mutually_exclusive_group() does not support setting a
        'title' or 'description' to the group, that might make it
        feasible to track at least which groups of arguments have been
        previously added. This issue may be partially resolved by naming
        the groups and tracking them manually in a dictionary attribute
        of the parser.

        Arguments:
          parser (ArgumentParser): Nascent argument parser
          name (str): Name of mutually exclusive group

        Returns:
          ?: Mutually exclusive group, either new or pre-existing
        """
        if not hasattr(parser, "_mutually_exclusive_group_dict"):
            parser._mutually_exclusive_group_dict = {}
        group = parser._mutually_exclusive_group_dict.get(name,
          parser.add_mutually_exclusive_group())
        return group

    @classmethod
    def get_help_arg_groups(class_, **kwargs):
        """
        """
        import sys

        if "--full-help" in sys.argv:
            help_groups = ["*"]
            sys.argv.pop(sys.argv.index("--full-help"))
            sys.argv += ["--help"]
        elif "--help" in sys.argv:
            help_groups = []
            argv_prehelp  = sys.argv[:sys.argv.index("--help")]
            argv_posthelp = list(sys.argv[sys.argv.index("--help")+1:])
            for i, arg in enumerate(argv_posthelp):
                if arg.startswith("-"):
                    break
                else:
                    help_groups += [arg]
            sys.argv = argv_prehelp + ["-h"] + argv_posthelp[i:]
        elif "-h" in sys.argv:
            help_groups = []
            argv_prehelp  = sys.argv[:sys.argv.index("-h")]
            argv_posthelp = sys.argv[sys.argv.index("-h")+1:]
            for i, arg in enumerate(argv_posthelp):
                if arg.startswith("-"):
                    break
                else:
                    help_groups += [arg]
            sys.argv = argv_prehelp + ["-h"] + argv_posthelp[i:]
        else:
            help_groups = []
        print(help_groups)
        return help_groups

    @classmethod
    def get_argparser(class_, parser=None, name=None, description=None, 
        grouped_help=False, **kwargs):
        """
        Arguments:
          parser (ArgumentParser, _SubParsersAction, optional): If
            ArgumentParser, existing parser to which arguments will be
            added; if _SubParsersAction, collection of subparsers to
            which a new argument parser will be added; if None, a new
            argument parser will be generated
          name (str, optional): Name of spec constructor
          description (str, optional): Description of spec constructor
          kwargs (dict): Additional keyword arguments

        Returns:
          ArgumentParser: Argument parser or subparser
        """
        import argparse
        from . import strfmt

        if name is None:
            if hasattr(class_, "name"):
                name = class_.name
            else:
                name = class_.__name__
        if description is None:
            if hasattr(class_, "description"):
                description = class_.description
            else:
                description = strfmt(class_.__doc__.split("\n\n")[0]) + "\n"

        if isinstance(parser, argparse.ArgumentParser):
            pass
        elif isinstance(parser, argparse._SubParsersAction):
            subparsers = parser
            parser = subparsers.add_parser(name=name, description=description,
              help=description)
        elif parser is None:
            if grouped_help:
                parser = argparse.ArgumentParser( description=description,
                  formatter_class=argparse.RawDescriptionHelpFormatter,
                  add_help=False)
                parser.add_argument(
                  "-h", "--help", "--full-help",
                  action = "help",
                  help   = """show this help message and exit; detailed help
                           for sections: {0} may be obtained by adding them as
                           arguments; while '--full-help' may be used to view
                           all available help """.format(str(map(str,
                           class_.help_groups)).replace("'","")))
            else:
                parser = argparse.ArgumentParser( description=description,
                  formatter_class=argparse.RawDescriptionHelpFormatter)

        return parser
