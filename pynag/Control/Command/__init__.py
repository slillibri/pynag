# -*- coding: utf-8 -*-
#
# pynag - Python Nagios plug-in and configuration environment
# Copyright (C) 2011 Pall Sigurdsson
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import time

from pynag.Parsers import config
import autogenerated_commands as __autogenerated_commands

def find_command_file(cfg_file=None):
    """ Returns path to nagios command_file by looking at what is defined in nagios.cfg """
    c = config(cfg_file=cfg_file)
    c.parse()
    command_file = None
    for k,v in c.maincfg_values:
        if k == 'command_file':
            command_file = v
            break
    if not command_file:
        if not command_file:
            raise PynagError("command_file not found in your nagios.cfg (%s)" % c.cfg_file)
    return command_file

def send_command(command_id, command_file=None, timestamp=0, *args):
    """ Send one specific command to the command pipe
    """
    if not timestamp or timestamp == 0:
        timestamp = time.time()
    if not command_file:
        command_file = find_command_file()
    command_arguments = map(str, args)
    command_arguments = ";".join(command_arguments)
    command_string = "[%s] %s;%s" % (timestamp, command_id, command_arguments)
    _write_to_command_file(command_file, command_string)
def _write_to_command_file(command_file, command_string=""):
    """ Send a specific command to nagios command pipe.

    See http://nagios.sourceforge.net/docs/nagioscore/3/en/extcommands.html for details
    """
    #print "writing to command pipe:", command_string
    #print "command_file:", command_file
    f = open(command_file, 'a')
    f.write(command_string + '\n')
    f.close()

# Everything in autogenerated_commands gets imported directly into this module.
filename = __autogenerated_commands.__file__
if filename.endswith('.pyc'):
    filename = filename.strip('c')
execfile(filename)