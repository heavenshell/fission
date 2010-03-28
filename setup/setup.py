#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Run command which is written in dsl.
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
from paver.easy import task, cmdopts, sh
import yaml
import os

class Assemble(object):
    """
    Run commands written in yaml file.
    """
    def __init__(self, options):
        """
        Get yaml file and command line options.
        """

        self.options = options
        self.yamlfile = './setup.yaml'
        self.command = None
        try:
            self.yamlfile = options['list']
        except KeyError:
            pass

        try:
            self.command = options['command'].split(',')
        except KeyError:
            pass

    def parse(self, filepath=None):
        """
        Parse yaml file.
        """
        if not filepath == None:
            self.yamlfile = filepath
        self.config = yaml.load(open(self.yamlfile))

        return self

    def run(self):
        """
        Run command.
        """
        configs = self.config or {}
        options = configs['options']
        if not options.get('build', None) == None:
            buildpath = options.get('build', None)
            print buildpath
            if not os.path.isdir(buildpath):
                os.makedirs(buildpath)
            os.chdir(buildpath)

        self.tasks = configs['task']

        _execute = lambda tasks : [
            sh(command) for task, commands in tasks.iteritems() for command in commands
        ]

        if self.command == None:
            for task in self.tasks:
                _execute(task)
        else:
            for command in self.command:
                for task in self.tasks:
                    if not task.get(command, None) == None:
                        _execute(task)
        return self

@task
@cmdopts([
    ('list=', 'l', 'Path to pear package list file.'),
    ('command=', 'c', 'Run commands.'),
])
def task(options):
    Assemble(options).parse().run()
