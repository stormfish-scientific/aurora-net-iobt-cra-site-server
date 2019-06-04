#!/usr/bin/python

# AURORA-Net IoBT CRA Site Server
# Copyright (C) 2019  Stormfish Scientific Corporation
#
# AURORA-Net IoBT CRA Site Server is free software: you can
# redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either
# version 3 of the License, or (at your option) any later version.
#
# AURORA-Net IoBT CRA Site Server is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

# By: Stormfish Scientific Corporation
# Author: Theron T. Tout
# For: CCDC ARL - US Army Research Laboratory, Battlefield Information
# Processing Branch
# Date: 2019-03-28


import configparser


class Config(object):

    def __init__(self, config_path):

        self.config_path = config_path

        self.config = configparser.ConfigParser()

        self.config.read(config_path)

    def __getitem__(self, i):

        if i not in self.config:
            return None

        return self.config[i]

    def __setitem__(self, i, v):
        self.config[i] = v

    def save(self):
        with open(self.config_path, "w") as configfile:
            self.config.write(configfile)

    def get(self, section, key, default=None):
        if section not in self.config:
            return default

        if key not in self.config[section]:
            return default

        return self.config[section][key]

    def set(self, section, key, value):
        self.config[section][key] = value

# if __name__ == '__main__':
#     conf = Config('test.conf')

#     print('section_1.a = ' + conf['section_1']['a'])

#     conf['section_1'] = {}

#     conf['section_1']['a'] = '123'

#     conf.save()
