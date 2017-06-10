#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from sys import exit

from ..libraries.project_check import ProjectCheck
from ..libraries.preferences_bridge import PreferencesBridge
from .run_command import run_command

class Initialize(ProjectCheck, PreferencesBridge):
    """
    Runs the init command to start working with a new board
    Initialize a new folder you need to know the board id
    and pass it as an argument in the class

    Initialize(board_id)

    The code will run in a new thread to avoid block the
    execution of the sublime text while platformio is working
    """
    def __init__(self):
        super(Initialize, self).__init__()

        self.board_id = self.get_environment()
        self.nonblock_add_board()

    def add_board(self, board_id):
        """New Board
        
        Adds a new board to the environments of platformio
        this new board will be stored in the platformio.ini
        file and will be use with the plugin
        
        Arguments:
            board_id {str} -- name of the board to initialize
        
        Returns:
            bool -- true if the board was succefully intilized or if it
                    was already initialized, if there was an error, false
        """
        if(not self.is_iot()):
            print("--Not IOT")
            exit(0)

        envs = self.get_envs_initialized()

        if(envs and self.board_id in envs):
            print("Initialized")
            return True

        cmd = ['init', '-b ', board_id]
        out = run_command(cmd, self.cwd, realtime=True)

        self.structurize_project()

    def nonblock_add_board(self):
        """New Thread Execution
        
        Starts a new thread to run the add_board method
        
        Arguments:
            board_id {str} -- id_of the board to initialize
        """
        from threading import Thread

        thread = Thread(target=self.add_board, args=(self.board_id,))
        thread.start()
        #thread.join()

