#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Run dsl command
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

class Assemble(object):
    """
    """
    def __init__(self, options):
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
        if not filepath == None:
            self.yamlfile = filepath
        self.config = yaml.load(open(self.yamlfile))

        return self

    def run(self):
        configs = self.config or {}
        options = configs['options']
        self.tasks = configs['task']
        for task in self.tasks:
            self.execute(task)

    def execute(self, tasks):
        def _execute(task):
            for task, commands in tasks.iteritems():
                for command in commands:
                    sh(command)

        if self.command == None:
            _execute(tasks)
        else:
            for command in self.command:
                if tasks.get(command, None) != None:
                    _execute(tasks.get(command))
        return self

@task
@cmdopts([
    ('list=', 'l', 'Path to pear package list file.'),
    ('command=', 'c', 'Run commands.'),
])
def task(options):
    assemble = Assemble(options)
    assemble.parse().run()
