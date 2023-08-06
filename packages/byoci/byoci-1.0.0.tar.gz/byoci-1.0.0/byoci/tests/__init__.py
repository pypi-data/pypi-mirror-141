# This file is part of Build Your Own CI
#
# Copyright 2018 Vincent Ladeuil
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 3, as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.
import os


HERE = os.path.abspath(os.path.dirname(__file__))


def load_tests(loader, std_tests, pattern):
    suite = loader.suiteClass()
    # Tests defined in /this/ file are always taken
    suite.addTests(std_tests)
    # As well as files defined in HERE
    names = os.listdir(os.path.abspath(HERE))
    names.remove('__init__.py')
    # Except if they have special requirements
    nodename = os.uname().nodename
    if nodename.startswith('brz-monitor'):
        # FIXME: Feedback about skipped tests is lost
        names.remove('host')
        names.remove('slave')
    elif nodename.startswith('brz-slave'):
        # FIXME: Revisit when finding the right credentials for either
        # production or qastaging becomes easier to do from the slave
        # -- vila 2018-02-20
        names.remove('host')
        names.remove('monitor')
    else:
        # That should be host ;-)
        names.remove('monitor')
    # Hard-coding 'byoci/tests' is not ideal but ideas welcome
    suite.addTests(loader.loadTestsFromFiles('byoci/tests', names))
    return suite
