#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Download arhive from Github
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
from paver.easy import task, cmdopts
from datetime import datetime
import os
import sys
import urllib
import tarfile
import shutil

GITHUB_URI = 'http://github.com'

@task
@cmdopts([
    ('uri=', 'u', 'Uri to github archive.'),
    ('dest=', 'd', 'Dest path to download archive.'),
    ('projectname=', 'p', 'Project name.')
])
def install(options):
    """
    Download tar.gz file from github project's master and extract to dest path.

    Usage:
      >>> paver -f /path/to/github.py install -u user/project
      >>> paver -f /path/to/github.py install -u user/project -d /path/to/dest
      >>> paver -f /path/to/github.py install -u user/project -p Projectname
    Arguments:
      options -- Command line options.
    """
    try:
        uri = options['uri']
    except KeyError:
        print 'Uri does not set. Done...'
        return

    dest = os.getcwd()
    try:
        dest = options['dest']
    except KeyError:
        pass

    if dest.endswith('/') == False:
        dest += '/'

    lists = uri.split('/')
    projectname = lists[len(lists) - 1]
    try:
        projectname = options['projectname']
    except KeyError:
        pass
    dest += projectname + '.tar.gz'

    download(uri, dest)
    expand(dest, projectname)

def _reporthook(blocknum, bs, size):
    filesize = blocknum * bs * 100 / size
    filesize = filesize if filesize < 100 else 100
    sys.stdout.write("Now downloading... %4d%%\r" % filesize)
    sys.stdout.flush()

def download(uri, dest):
    if not uri.startswith('/'):
        uri = '/' + uri

    uri = GITHUB_URI + uri + '/tarball/master'
    print datetime.now()
    print 'Download archive from: ' + uri
    urllib.urlretrieve(uri, dest, _reporthook)
    print

def expand(filepath, projectname):
    if not tarfile.is_tarfile(filepath):
        print 'Not a tar.gz archive file.'
        return
    print 'Extracting ' + filepath
    basename = filepath[:filepath.rfind('/') + 1]
    os.chdir(basename)

    tar = tarfile.open(filepath, 'r')
    dirname = tar.getmembers()[0].name if len(tar.getmembers()) > 0 else ''
    if dirname == '':
        print 'Fail to get tar file member.'
        return
    tar.extractall()
#    for item in tar:
#        print item.name
#        tar.extract(item)

    tar.close()
    dirname = basename + dirname
    if os.path.exists(dirname):
        ret = shutil.move(dirname, basename + projectname)
        os.remove(filepath);

    print 'Done...'
    return
