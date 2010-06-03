#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    fission.setup.Assemble
    ~~~~~~~~~~~~~~~~~~~~~~

    Run command which is written in dsl.

    :copyright: (c) 2010 Shinya Ohyanagi, All rights reserved.
    :license: BSD, see LICENSE for more details.
"""
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

        Arguments:

        * options: Command line options
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

        Arguments:

        * filepath: Path to file.
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
