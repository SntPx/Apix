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
""" Qt Window for pxmgr

Main window for pxmgr GUI

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

import os
from PyQt6 import QtWidgets, uic, QtCore, QtGui
from decimal import *
from backendData.csvReader import csv_read, populate_pupils
from edu.Domain import Domain, Skill
from collections import deque
import datetime
from __init__ import __version__


class Ui(QtWidgets.QMainWindow):
    def __init__(self, ):
        super(Ui, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'mainWindow.ui'), self)

        self.pupilDetail.setModel(QtGui.QStandardItemModel())  # Set a standard model on our QTreeView (details)

        self.KYTITLE = f"Butineur Apix v{__version__}"  # This is the base title for our main window
        self.setWindowTitle(self.KYTITLE)  # Set base title for main window

        self.csv_data = ''  # A list, that will contain all the data read and extracted from CSV file

        self.pupilList.setModel(QtGui.QStandardItemModel())  # Set a standard model on our QListView (names)

        self.pupilList.selectionModel().selectionChanged.connect(self.change_pupil
                                                                 )  # Set action to launch on name selection
        self.certifiableRadio.toggled.connect(self.populate_list
                                              )  # Set action to launch when toggling certifiable radio to ON
        self.nonCertifiableRadio.toggled.connect(self.populate_list
                                                 )  # Set action to launch when toggling non certifiable radio to ON
        self.scoreSpinBox.valueChanged.connect(self.populate_list
                                               )  # Set action to launch on changing value for threshold level
        self.browseButton.clicked.connect(self.open_file
                                          )  # Set action to launch on clicking the Browse button

        self.show()

    def change_pupil(self, selected, deselected):
        """
        This changes the contents of the pupilDetail QTreeView widget
        :param selected: the selected line in QListView
        :param deselected: the deselected line in QListView
        :return:
        """
        role = QtCore.Qt.ItemDataRole.DisplayRole
        color_role = QtCore.Qt.ItemDataRole.ForegroundRole
        parent = self.pupilDetail.model()

        for i in selected.indexes():

            pupil = list(filter(lambda p: ' '.join((getattr(p, 'Nom'),
                                                    getattr(p, 'Prénom'))) == i.data(), self.csv_data)
                         )[0]  # a Pupil instance stored in self.csvData

            if parent.rowCount() > 0:  # If the QTreeView is not empty, let's empty it
                for x in reversed(range(parent.rowCount())):  # Had to reverse to make sure only old entries were deleted
                    parent.removeRow(x)

            excludes = [
                "Nom", "Prénom", "Classe", "Progression", "shared"
            ]

            color = ''
            elements = deque()

            for (attr_name, attr_val) in pupil.__dict__.items():  # Ugly, but acceptable for a very early version
                if attr_name not in excludes:
                    if attr_name != "crcn":
                        if attr_name == 'Partage le':
                            shareDateNameItem = QtGui.QStandardItem()
                            shareDateNameItem.setEditable(False)
                            shareDateNameItem.setData('Profil partagé le', role)
                            shareDateValItem = QtGui.QStandardItem()
                            shareDateValItem.setEditable(False)
                            if type(attr_val) is datetime.date:
                                shareDateValItem.setData(attr_val.strftime('%d/%m/%Y'), role)
                            if type(attr_val) is not datetime.date:
                                shareDateValItem.setData('Non rendu', role)
                            elements.appendleft([
                                shareDateNameItem,
                                shareDateValItem
                            ])
                        if attr_name == "profil":
                            attr_name = 'Score général'
                            n_attr_val = attr_val
                            if Decimal(attr_val.replace(',', '.')) < 0:
                                n_attr_val = 'Non disponible'
                            if Decimal(attr_val.replace(',', '.')) > 0:
                                n_attr_val = f"{Decimal(attr_val.replace(',', '.').format('.2f'))}%"
                            profilNameItem = QtGui.QStandardItem()
                            profilNameItem.setData(attr_name, role)
                            profilNameItem.setEditable(False)
                            profilValItem = QtGui.QStandardItem()
                            profilValItem.setData(n_attr_val, role)
                            profilValItem.setEditable(False)
                            elements.appendleft([
                                profilNameItem,
                                profilValItem
                            ])

                        if attr_val == '-1':
                            attr_val = 'NA'
                        else:
                            attr_val = f'{attr_val}%'
                    elif attr_name == "crcn":  # TODO: Arrange domains in th order of their rank (Domain.rank)
                        for d, v in attr_val.items():
                            _color = Domain.get(d).color
                            color = QtGui.QColor(_color[0], _color[1], _color[2], 255)
                            domainNameItem = QtGui.QStandardItem()
                            domainNameItem.setData(d, role)
                            domainNameItem.setData(color, color_role)
                            domainNameItem.setEditable(False)
                            domainValItem = QtGui.QStandardItem()
                            if v['score'] == '-1':
                                domainValItem.setData('Non rendu', role)
                                domainValItem.setData(color, color_role)
                            if v['score'] != '-1':
                                domainValItem.setData(f"{v['total']}/{v['nb']} ("
                                                      f"{Decimal(v['score'].replace(',', '.')) * 100})%", role)
                            domainValItem.setData(color, color_role)
                            domainValItem.setEditable(False)
                            for s, sv in attr_val[d]['skills'].items():
                                skillNameItem = QtGui.QStandardItem()
                                skillNameItem.setData(s, role)
                                skillNameItem.setEditable(False)
                                skillNameItem.setToolTip(s)
                                skillValItem = QtGui.QStandardItem()
                                if sv['score'] != 'NA':
                                    skillValItem.setEditable(False)
                                    skillValItem.setData(f"{sv['total']}/{sv['nb']} ("
                                                         f"{Decimal(sv['score'].replace(',', '.')) * 100}%)", role)
                                if sv['score'] == 'NA':
                                    skillValItem.setEditable(False)
                                    skillValItem.setData('Non disponible', role)
                                if sv['score'] == '-1':
                                    skillValItem.setData('Non rendu', role)
                                domainNameItem.appendRow([
                                    skillNameItem,
                                    skillValItem
                                ])

                            elements.append([domainNameItem, domainValItem])
            for elem in elements:
                self.pupilDetail.model().appendRow(elem)

            self.pupilDetail.setColumnWidth(0, 350)  # Change column width to make attr name readable

    def show_certifiable(self, data):
        """
        Action to perform to show all profiles, that passed the test
        :param data: a Pupil instance
        :return:
        """
        if Decimal(
                getattr(data, 'profil')
        ) >= self.scoreSpinBox.value() and getattr(data, 'shared') is True:
            item = QtGui.QStandardItem(' '.join((getattr(data, 'Nom'),
                                                 getattr(data, 'Prénom'))))
            self.pupilList.model().appendRow([item])

    def show_non_certifiable(self, data):
        """
        Action to perform to show all profiles, that did not pass the test
        :param data: a Pupil instance
        :return:
        """
        if Decimal(
            getattr(data, 'profil')
        ) < self.scoreSpinBox.value():
            item = QtGui.QStandardItem(' '.join((getattr(data, 'Nom'),
                                                 getattr(data, 'Prénom'))))
            if getattr(data, 'shared') is False:  # Profile did not share their results
                item.setData(QtGui.QColor('dark red'), QtCore.Qt.ItemDataRole.ForegroundRole)  # Appear in dark red
            if getattr(data, 'Progression') != '100':  # Profile hasn't finished the test
                item.setData(QtGui.QColor('red'), QtCore.Qt.ItemDataRole.ForegroundRole)  # Appear in red
            # If profile finished the test and shared their result, they appear in black
            self.pupilList.model().appendRow([item])

    def populate_list(self):
        """
        Insert names of pupils in QListView, depending of their having passed the test and shared their result
        :return:
        """
        self.empty_widget(self.pupilList.model())  # Empty QListView
        self.empty_widget(self.pupilDetail.model())  # Empty QTreeView
        for pupil in self.csv_data:
            if self.certifiableRadio.isChecked():
                self.show_certifiable(pupil)
            if self.nonCertifiableRadio.isChecked():
                self.show_non_certifiable(pupil)

    def empty_widget(self, model):
        """
        Utility method to empty any Q*View Widget
        :param model: a widget model
        :return:
        """
        for x in reversed(range(model.rowCount())):
            model.removeRow(x)

    def open_file(self):
        """
        Opens a CSV file, reads it and populates views as needed.
        :return:
        """
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Sélectionner la source", '.', 'Fichiers CSV (*.csv)')
        if path != ('', ''):
            self.filePathWidget.setText(path[0])
        h, d = csv_read(path[0], delimiter=';')
        self.csv_data = populate_pupils(h, d)
        self.populate_list()
        self.setWindowTitle(f"{self.KYTITLE} - {os.path.basename(path[0])}")  # Modify window title
