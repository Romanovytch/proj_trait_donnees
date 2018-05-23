# -*- coding: utf-8 -*-
"""
Created on Wed May 16 18:28:37 2018

@author: id1043
"""

class Error:
    def __init__(self, msg):
        self.error_msg = '\n\n' + ' '*10 + '\x1b[31m\x1b[1m' + '[ \u26A0 ERROR: ' + msg + ' \u26A0 ]' + '\x1b[0m' + '\n\n'
    
    def display(self):
        print(self.error_msg)