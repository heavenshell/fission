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
from paver.easy import task, cmdopts, path, sh
from datetime import datetime
import os
import sys
import urllib
import tarfile
import zipfile
import shutil

def _reporthook(blocknum, bs, size):
    """
    Callback function for show download progress.

    Arguments:
        blocknum -- Download block file number
        bs -- Block size
        size -- Package size
    """
    filesize = blocknum * bs * 100 / size
    filesize = filesize if filesize < 100 else 100
    sys.stdout.write("Now downloading... %4d%%\r" % filesize)
    sys.stdout.flush()

def _download(uri, dest):
    """
    Download package file

    Arguments:
        uri -- Package file uri
        dest -- Path to download
    """

    print 'Download archive from: ' + uri
    urllib.urlretrieve(uri, dest, _reporthook)
    print

def _expand(filepath):
    """
    Extract tar or zip file.

    Arguments:
        filepath -- Path to tar/zip file
    Return:
        Extract archive path
    """

    if tarfile.is_tarfile(filepath):
        fileobject = tarfile
    elif zipfile.is_zipfile(filepath):
        fileobject = zipfile
    else:
        print 'File is not a tar or zip archive.'
        return

    print 'Extracting ' + filepath
    basename = filepath[:filepath.rfind('/') + 1]
    os.chdir(basename)

    archive = fileobject.open(filepath, 'r')

    ## Todo: Fix to get only target file/dirctory
    dirname = archive.getmembers()[0].name if len(archive.getmembers()) > 0 else ''

    if dirname == '':
        print 'Fail to get archive file member.'
        return
    archive.extractall()

    archive.close()
    dirname = basename + dirname
    os.remove(filepath)

    return dirname

def move(source, dest, projectname, targets):
    """
    Move files to dest path

    Arguments:
        source -- From
        dest -- To
        projectname -- Replace directory/file name
        targets --
    """
    if projectname == '' and targets == '':
        filepath, ext = os.path.splitext(dest)
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath))
        sh('cp -f -R %s %s' % (source, dest))

    else:
        if targets == '':
            dest = dest.rstrip('/') + '/' + projectname
            sh('cp -f -R %s %s' % (source, dest))
        else:
            for target in targets:
                item = source.rstrip('/') + '/' + target

                if os.path.exists(item):
                    destpath = dest.rstrip('/') + '/' +  projectname + '/' + target

                    if not os.path.exists(destpath):
                        os.makedirs(destpath)
                    sh('cp -f -R %s %s' % (item,  destpath))

def _execute(text, buildpath):
    """
    Download packages, extract files and move to dest path.

    Arguments:
        text -- Package uri, dest path, package name, target files to move.
        buildpath -- Path to download direcotry
    """

    if text.startswith('#'):
        return

    sources = text.split(',')
    uri = sources[0].rstrip(' ')
    dest = sources[1].lstrip(' ')
    try:
        projectname = sources[2].lstrip(' ')
    except Exception, e:
        projectname = ''

    try:
        targets = sources[3].lstrip(' ').split(' ')
    except Exception, e:
        targets = ''


    build = buildpath + os.path.basename(uri)
    print
    _download(uri, build)
    dirname = _expand(build)
    move(dirname, dest, projectname, targets)
    print

@task
@cmdopts([('list=', 'l', 'Path to pear package list file.')])
def install(options):
    """
      Download packages from list.

      >>> paver -f package.py install -l list.txt
    """
    print datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    try:
        file = options['list']
    except KeyError:
        file = './list.txt'

    buildpath = os.getcwd() + '/build/'
    if not os.path.exists(buildpath):
        os.makedirs(buildpath)

    file = path(file)
    if file.isfile():
        for line in file.lines():
            try:
                _execute(line.rstrip(), buildpath)
            except Exception, e:
                print e
    #shutil.rmtree(buildpath.rstrip('/'))
    print 'Build success. All tasks went fine.'
