import sys
import argparse

import heron.ui.src.python.consts as consts

class _HelpAction(argparse._HelpAction):
  def __call__(self, parser, namespace, values, option_string=None):
    parser.print_help()

    # retrieve subparsers from parser
    subparsers_actions = [
      action for action in parser._actions
      if isinstance(action, argparse._SubParsersAction)]

    # there will probably only be one subparser_action,
    # but better save than sorry
    for subparsers_action in subparsers_actions:
      # get all subparsers and print help
      for choice, subparser in subparsers_action.choices.items():
        print("Subparser '{}'".format(choice))
        print(subparser.format_help())

    parser.exit()

class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
  def _format_action(self, action):
    parts = super(argparse.RawDescriptionHelpFormatter, self)._format_action(action)
    if action.nargs == argparse.PARSER:
      parts = "\n".join(parts.split("\n")[1:])
    return parts

def add_titles(parser):
  parser._positionals.title = "Required arguments"
  parser._optionals.title = "Optional arguments"
  return parser

def add_arguments(parser):
  parser.add_argument(
      '--tracker_url',
      metavar='(a url; path to tracker; default: "' + consts.DEFAULT_TRACKER_URL + '")',
      default=consts.DEFAULT_TRACKER_URL)

  parser.add_argument(
      '--port',
      metavar='(an integer; port to listen; default: ' + str(consts.DEFAULT_PORT) + ')',
      type = int, 
      default=consts.DEFAULT_PORT)

  return parser

def create_parsers():
  parser = argparse.ArgumentParser(
      epilog = 'For detailed documentation, go to http://go/heron',
      usage = "%(prog)s [options] [help]",
      add_help = False)

  parser = add_titles(parser)
  parser = add_arguments(parser)

  # create the child parser for subcommand
  child_parser = argparse.ArgumentParser(
      parents = [parser],
      formatter_class=SubcommandHelpFormatter,
      add_help = False)

  # subparser for each command
  subparsers = child_parser.add_subparsers(
      title = "Available commands")
  
  help_parser = subparsers.add_parser(
      'help',
      help='Prints help',
      add_help = False)

  help_parser.set_defaults(help=True)
  return (parser, child_parser)
