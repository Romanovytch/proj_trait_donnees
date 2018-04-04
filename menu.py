import os
from data import *

class Menu:
	def __init__(self, lib):
        	self.choices = {}
        	self.user_ch = 0
		self.lib = []
        
	def disp_menu(self):
		os.system('cls')
        	os.system('clear')
		print("#"*50+"\n"+"#"+" "*22+"MENU"+" "*22+"#"+"\n"+"#"*50)
        	for i in range(len(self.choices)):
            		print(str(i+1)+". "+self.choices[str(i+1)])

    	def user_input(self):
        	while str(self.user_ch) not in self.choices.keys():
            		print('-'*50+"\nVeuillez entrer un nombre parmi {}".format(', '.join(str(i+1) for i in range(len(self.choices)))))
			self.user_ch = input("Choix utilisateur : ")
		if self.user_ch == 1:
			lib_menu = LibMenu(lib)
        
class LibMenu(Menu):
	def __init__(self, library):
		Menu.__init__(self, library)
		self.choices = dict()
		for i in range(len(library.lib)):
			self.choices[str(i+1)] = library.lib[i].name
		self.choices[str(i+1)] = "Retour"
		self.choices[str(i+2)] = "Quitter"

class MainMenu(Menu):
	def __init__(self, lib):
        	Menu.__init__(self, lib)
        	self.choices = {"1":"Visualiser les donnees",
                        	"2":"Creer une sous-population",
                        	"3":"Traitement statistique",
                        	"4":"Modifier une base",
                        	"5":"Quitter"}

	def show_bdd(self):
		lib_menu = LibMenu(lib)
		lib_menu.disp_menu()

lib = Library()
lib.add_db(BaseDeDonnees("vinData.json"))
main_menu = MainMenu(lib)
main_menu.disp_menu()
main_menu.user_input()
