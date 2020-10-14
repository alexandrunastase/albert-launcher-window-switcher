# -*- coding: utf-8 -*-

"""List and manage X11 windows.
Synopsis: <filter>"""

import subprocess
from collections import namedtuple
from shutil import which

from albertv0 import Item, ProcAction, iconLookup

Window = namedtuple("Window", ["wid", "desktop","wm_class", "host", "wm_name"])

__iid__ = "PythonInterface/v0.1"
__prettyname__ = "Window Switcher - forked"
__version__ = "1.4"
__author__ = "Ed Perez, Manuel Schneider, Alexandru Năstase"
__dependencies__ = ["wmctrl"]

if which("wmctrl") is None:
    raise Exception("'wmctrl' is not in $PATH.")

def handleQuery(query):
    if not query.string.strip():
        defaultResults = []
        for line in subprocess.check_output(['wmctrl', '-l', '-x']).splitlines():
            win = Window(*[token.decode() for token in line.split(None, 4)])
            if "albert" in win.wm_name and "Albert" in win.wm_name:
                continue

            if win.desktop != "-1":
                defaultResults.append(Item(id="%s%s" % (__prettyname__, win.wm_class),
                                           icon=iconLookup(
                                               win.wm_class.split('.')[1].capitalize()),
                                           text="%s" % (win.wm_class.split('.')[0].capitalize()),
                                           subtext=win.wm_name,
                                           actions=[ProcAction("Switch Window",
                                                               ["wmctrl", '-i', '-a', win.wid]),
                                                    ProcAction("Move window to this desktop",
                                                               ["wmctrl", '-i', '-R', win.wid]),
                                                    ProcAction("Close the window gracefully.",
                                                               ["wmctrl", '-c', win.wid])]))
        return defaultResults

    stripped = query.string.strip().lower()
    if stripped:
        results = []
        for line in subprocess.check_output(['wmctrl', '-l', '-x']).splitlines():
            win = Window(*[token.decode() for token in line.split(None, 4)])
            if "albert" in win.wm_name and "Albert" in win.wm_name:
                continue
            if win.desktop != "-1" and stripped in win.wm_name.lower():
                results.append(Item(id="%s%s" % (__prettyname__, win.wm_class),
                                       icon=iconLookup(
                                           win.wm_class.split('.')[1].capitalize()),
                                       text="%s" % (win.wm_class.split('.')[0].capitalize()),
                                       subtext=win.wm_name,
                                       actions=[ProcAction("Switch Window",
                                                           ["wmctrl", '-i', '-a', win.wid]),
                                                ProcAction("Move window to this desktop",
                                                           ["wmctrl", '-i', '-R', win.wid]),
                                                ProcAction("Close the window gracefully.",
                                                           ["wmctrl", '-c', win.wid])]))
        return results
