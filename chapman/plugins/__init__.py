#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Chapman plugin management."""

# Taken from Python 2.7 via django 1.1
import sys
from chapman import core

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.
    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

def get_available_plugins():
    """Return a list of available plugins."""
    import os
    plugin_path = os.path.dirname(__file__)
    plugin_files = [f for f in os.listdir(plugin_path) if f.endswith('.py') and os.path.isfile(f)]
    plugins = []
    for path in plugin_files:
        plugin_module = import_module(path[:-3])
        for obj in plugin_module.__dict__.values():
            if issubclass(obj, core.ChapmanPlugin):
                plugins.append(obj)
    return plugins
