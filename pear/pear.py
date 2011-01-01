#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    fission.pear
    ~~~~~~~~~~~~

    Install pear package from pear.txt

    :copyright: (c) 2010-2011 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
from paver.easy import task, cmdopts, sh, path

def _execute(text):
    """
    Execute pear command.

    Arguments:

    * text: Pear package name
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

    * options['file']: Path to pear package list file

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
