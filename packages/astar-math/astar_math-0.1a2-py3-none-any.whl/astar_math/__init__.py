# -*- coding: utf-8 -*-

from astar_devopstool.version_announcement import get_version

version = (0, 1, 0, 'alpha', 2)
__version__ = get_version(version)

del get_version
