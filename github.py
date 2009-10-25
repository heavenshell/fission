#!/usr/bin/env python
# -*- coding: utf_8 -*-
from paver.easy import *
import os
import sys
import urllib
import tarfile
import shutil

GITHUB_URI = 'http://github.com/'

@task
@cmdopts([
    ('uri=', 'u', 'Uri to github archive.'),
    ('dest=', 'd', 'Dest path to download archive.'),
    ('projectname=', 'p', 'Project name.')
])
def install(options):
    """
    Download tarball github project's master archive.

    Usage:
        >>> paver -f /path/to/github.py install -u username/projectname
    """
    try:
        uri = options['uri']
    except KeyError:
        print 'Uri does not set. Done...'
        return

    dest = os.getcwd() + '/'
    try:
        dest = options['dest']
    except KeyError:
        pass

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
    sys.stdout.write("Download %4d%%\r" % filesize)
    sys.stdout.flush()

def download(uri, dest):
    uri = GITHUB_URI + uri + '/tarball/master'
    print 'Download archive from: ' + uri
    urllib.urlretrieve(uri, dest, _reporthook)
    print

def expand(filepath, projectname):
    if not tarfile.is_tarfile(filepath):
        print 'Not a tar.gz archive file.'
        return
    print 'Extracting tar.gz...'
    basename = filepath[:filepath.rfind('/') + 1]

    tarhandler = tarfile.open(filepath, 'r')
    dirname = tarhandler.getmembers()[0].name if len(tarhandler.getmembers()) > 0 else ''
    if dirname == '':
        print 'Fail to get tar file member.'
        return
    tarhandler.extractall()
#    for item in tarhandler:
#        print item.name
#        tarhandler.extract(item)

    tarhandler.close()
    dirname = basename + dirname
    if os.path.exists(dirname):
        shutil.move(dirname, basename + projectname)
    print 'Done...'
    return
