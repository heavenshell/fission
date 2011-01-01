#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    fission.github
    ~~~~~~~~~~~~~~

    Download tar.gz file from Github project.

    :copyright: (c) 2010-2011 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
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

    * options: Command line options.
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
