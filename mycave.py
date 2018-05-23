# -*- coding: utf-8 -*-
"""
Created on Wed May 16 23:31:41 2018

@author: id1043
"""

import menu
import db

lib = db.Library()
lib.add_db(db.BaseDeDonnees("vinData.json"))
main_menu = menu.MainMenu(lib)
main_menu.start()