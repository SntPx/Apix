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
""" Csv reader for pxmgr

CSV reading logic for pxmgr

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
import csv
import logging
from edu.Pupil import Pupil
from edu.Domain import Skill, get_domains
from decimal import *
import datetime
import re

DEBUG = False


def populate_pupils(headers, data):

    pc_pattern = re.compile(r"^% (?:de )?(?P<maitrise>maitrise) (?:de l'ensemble\s)?des acquis (?:du\s|de\sla\s)?"
                            r"(?P<type>domaine|compétence|\s)?\s?(?P<sdp>[\w\-'\s,]+)$", re.U)
    nb_pattern = re.compile(r"Nombre d'acquis du profil cible (?:dans la |du )(?P<type>compétence|domaine) "
                            r"(?P<sd>[\w\-,'\s]+)$", re.U)
    total_pattern = re.compile(r"Acquis maitrisés (:?dans la |du )(?P<type>compétence|domaine) (?P<sd>[\w\-,'\s]+)$",
                               re.U)
    name_pattern = re.compile(r"^(?P<Name>(:?Pré)?(?:N|n)om) du Participant$", re.U)
    pupil_lst = []

    domains = get_domains()  # Load the list of Domain instances generated from JSON

    for my_data in data:
        attr_count = 0
        pupil = Pupil()  # Instanciate Pupil
        setattr(pupil, 'crcn', {})  # Add attribute crcn to pupil
        color = None
        # Now, let's populate crcn attribute with data from ou list of Domain instances
        for d in domains:
            pupil.crcn[d.name] = {
                'nb': 'NA',
                'total': 'NA',
                'score': 'NA',
                'skills': {}
            }
            for s in d._skills:
                pupil.crcn[d.name]['skills'][s.name] = {
                    'nb': 'NA',
                    'total': 'NA',
                    'score': 'NA'
                }
        for attr in my_data:

            if attr == "NA":
                attr = "-1"

            header_attr = headers[attr_count]
            personal_info = name_pattern.match(header_attr)
            percent = pc_pattern.match(header_attr)
            nb = nb_pattern.match(header_attr)
            total = total_pattern.match(header_attr)

            if header_attr == "% de progression":
                attr = f'{Decimal(attr.replace(",", ".")) * 100}'.format({'%.f2'})
                setattr(pupil, 'Progression', attr)

            if header_attr == "Date du partage":
                if attr != '-1':
                    (y, m, d) = attr.split('-')
                    attr = datetime.date(int(y), int(m), int(d))
                setattr(pupil, 'Partage le', attr)

            if header_attr.startswith('Partage'):
                if attr == 'Oui':
                    setattr(pupil, 'shared', True)
                else:
                    setattr(pupil, 'shared', False)

            if personal_info:
                setattr(pupil, personal_info.group('Name'), attr)

            if percent:
                if percent.group('type') is None:
                    # This should match the profile
                    attr = f'{Decimal(attr.replace(",", ".")) * 100}'.format({'%.f2'})
                    setattr(pupil, percent.group('sdp'), attr)
                elif percent.group('type') is not None:
                    if percent.group('type') == 'domaine':
                        pupil.crcn[percent.group('sdp')]['score'] = attr
                    if percent.group('type') == 'compétence':
                        skill = percent.group('sdp')
                        pupil.crcn[Skill.get(skill).get_domain().name]['skills'][skill]['score'] = attr
            if nb:
                if nb.group('type') == "domaine":
                    pupil.crcn[nb.group('sd')]['nb'] = attr
                if nb.group('type') == "compétence":
                    skill = nb.group('sd')
                    pupil.crcn[Skill.get(skill).get_domain().name]['skills'][skill]['nb'] = attr

            if total:
                if total.group('type') == "domaine":
                    pupil.crcn[total.group('sd')]['total'] = attr
                if total.group('type') == "compétence":
                    skill = total.group('sd')
                    pupil.crcn[Skill.get(skill).get_domain().name]['skills'][skill]['total'] = attr

            attr_count += 1
        pupil_lst.append(pupil)
    return pupil_lst


def csv_read(filename, delimiter=","):
    csv_headers = None
    csv_data = []
    try:
        with open(filename, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    r = row[0].replace("\uFEFF", '')
                    row[0] = r
                    if DEBUG:
                        print(f'Columns are: {",".join(row)}')
                    csv_headers = [x.replace(chr(8217), chr(39)) for x in row]  # Had to replace chr(8217) with chr(39)
                                                                                # because Pix team doesn't know to use
                                                                                # raw unbeautified data...
                    line_count += 1
                else:
                    if DEBUG:
                        print(f'Data row # {line_count}: {",".join(row)}')
                    csv_data.append(row)
                    line_count += 1
    except FileNotFoundError as e:
        if e.filename == '':
            pass
    return csv_headers, csv_data
