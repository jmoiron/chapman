#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Chapman script support."""

import os

from cmdparse import Command, CommandParser

class ListCommand(Command):
    def __init__(self):
        Command.__init__(self, "list", summary="list various parts of the system")

    def run(self, options, args):
        if not args:
            print "Available lists:"
            print " * plugins"
        elif args[0] == 'plugins':
            from chapman.plugins import get_available_plugins
            plugins = get_available_plugins()
            if plugins:
                print "Plugins:"
                print " * " + '\n * '.join([p.name for p in plugins])
            else:
                print "No installed plugins."
        else:
            print "Unknown list option: %s" % str(args)

def main():
    parser = CommandParser(usage="%prog [command]", version='0.1')
    parser.add_command(ListCommand())
    command, opts, args = parser.parse_args()
    if command is None:
        parser.print_help()
        return 1
    return command.run(opts, args)
    return 0

