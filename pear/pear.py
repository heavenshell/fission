#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Install pear package from pear.txt
#
# Copyright (c) 2009-2010 Shinya Ohyanagi, All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#   * Neither the name of Shinya Ohyanagi nor the names of his
#     contributors may be used to endorse or promote products derived
#     from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
from paver.easy import task, cmdopts, sh, path

def _execute(text):
    """
    Execute pear command.

    Arguments:
        text -- Pear package name
    """
    if text.find('channel-discover') == -1:
        print 'install pear package...'
        sh('sudo pear install ' + text)
    else:
        sh('sudo pear ' + text)
    return

@task
@cmdopts([('list=', 'l', 'Path to pear package list file.')])
def install(options):
    """
    Install PHP's PEAR package which read from list file.

    Arguments:
        options['file'] -- Path to pear package list file

    Usage:
        >>> paver -f /path/to/pear.py install -l /path/to/pear.txt
    """
    try:
        file = options['list']
    except KeyError:
        file = './pear.txt'

    file = path(file)
    if file.isfile():
        for line in file.lines():
            try:
                _execute(line.rstrip())
            except:
                pass
