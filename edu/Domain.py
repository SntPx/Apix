#!/usr/bin/python3
#
# Copyright (c) 2021-2022 Christophe 'SntPx' RIVIERE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
""" Dummy Pupil class for pxmgr

Dummy Pupil class for pxmgr

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Christophe 'SntPx' RIVIERE"
__contact__ = "sntpx@meltdown.fr"
__copyright__ = "Copyright 2021, Christophe 'SntPx' RIVIERE"
__date__ = "2021/12/14"
__deprecated__ = False
__email__ = "meltdownfr@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "Christophe 'SntPx' RIVIERE"
__status__ = "Production"
__version__ = "1.0.0"

import uuid
import os
import json
import errno


class Skill:

    ky_instances = []

    def __init__(self):
        self.id = uuid.uuid4()
        self.__class__.ky_instances.append(self)
        self._domain = None

    def __str__(self):
        if hasattr(self, 'name'):
            return f"Skill <{self.name}>"
        return f"Skill {self.id}"

    def __repr__(self):
        if hasattr(self, 'name'):
            return f"Skill <{self.name}>"
        return f"Skill {self.id}"

    def get_domain(self):
        return Domain.get(self._domain)

    @classmethod
    def instances(cls):
        return cls.ky_instances

    @classmethod
    def get(cls, skill):
        for s in cls.instances():
            if s.name == skill:
                return s
        return


class Domain:

    ky_instances = []

    def __init__(self):
        self.id = uuid.uuid4()
        self.__class__.ky_instances.append(self)
        self.name = ''
        self._skills = []

    def __str__(self):
        if not self.name:
            return f"Domain <{self.id}>"
        return f"Domain <{self.name}>"

    def __repr__(self):
        if not self.name:
            return self.__str__()
        return f"Domain {self.name}"

    def add_skill(self, skill):
        if not isinstance(skill, Skill):
            raise TypeError(f"Could not add {skill} to {self}: only Skill() instances are accepted")

        if not hasattr(skill, 'name'):
            raise ValueError(f'Could not add {skill} to {self}: the skill has not been initialized with a name')

        if not hasattr(self, 'name'):
            raise ValueError(f'Could not add {skill} to {self}: your Domain has no name')

        self._skills.append(skill)
        skill._domain = self.name

    def get_skills(self):
        return self._skills

    @classmethod
    def instances(cls):
        return cls.ky_instances

    @classmethod
    def get(cls, domain):
        for d in cls.instances():
            if d.name == domain:
                return d
        return


def create_domains_skills():
    """
    Create all Domain and Skill classes needed. Skills and domains have their names harcoded.
    :return:
    """
    try:
        with open(os.path.join(
            os.path.dirname(os.path.pardir),
            'res', 'crcn.json'
        ), encoding='utf-8') as jsonfile:
            jsondata = json.load(jsonfile)
            for domain, data in jsondata.items():
                d = Domain()
                d.name = domain
                d.color = data['color']
                d.rank = data['rank']
                for skill in data['skills']:
                    s = Skill()
                    s.name = skill
                    d.add_skill(s)
    except IOError as x:
        if x.errno == errno.ENOENT:
            print(f'File {jsonfile} does not exist!')
        elif x.errno == errno.EACCES:
            print(f'File {jsonfile} cannot be read!')


def get_domains():
    """
    Returns a list of all Domain instances created.
    :return: a list of all Domain instances created
    """
    return Domain.instances()
