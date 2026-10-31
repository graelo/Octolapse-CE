# coding=utf-8
##################################################################################
# Octolapse - A plugin for OctoPrint used for making stabilized timelapse videos.
# Copyright (C) 2023  Brad Hochgesang
##################################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see the following:
# https://github.com/FormerLurker/Octolapse/blob/master/LICENSE
#
# You can contact the author either through the git-hub repository, or at the
# following email address: FormerLurker@pm.me
##################################################################################

"""Vendored minimal LooseVersion.

distutils was removed from the Python standard library in 3.12 and only still
works accidentally, through the setuptools ``distutils`` shim (which also emits
deprecation warnings and is scheduled for removal). Octolapse's
``NumberedVersion`` needs the exact component-wise comparison semantics of
``distutils.version.LooseVersion`` for settings migration, including for
non-PEP440 strings like ``0.4.5+3.g9ff3cbe`` or ``unknown`` — ``packaging``'s
``Version`` cannot parse those. So we vendor the (tiny, PSF-licensed)
parsing/comparison core of distutils' LooseVersion here.

Source: Python's ``distutils/version.py`` (PSF license). Trimmed to the parts
``NumberedVersion`` relies on (``__init__``, ``parse``, ``self.version``);
``NumberedVersion`` defines all ordering operators itself.
"""

import re


class LooseVersion:
    component_re = re.compile(r"(\d+ | [a-z]+ | \.)", re.VERBOSE)

    def __init__(self, vstring=None):
        if vstring:
            self.parse(vstring)

    def parse(self, vstring):
        self.vstring = vstring
        components = [x for x in self.component_re.split(vstring) if x and x != "."]
        for i, obj in enumerate(components):
            try:
                components[i] = int(obj)
            except ValueError:
                pass
        self.version = components
