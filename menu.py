import os
from data import *

class Menu:
	def __init__(self, lib):
        	self.choices = {}
        	self.user_ch = 0
		self.lib = lib
		self.name = "Menu"
        
	def disp_menu(self):
		os.system('cls')
        	os.system('clear')
		print("#"*50+"\n"+"#"+" "*22+"MENU"+" "*22+"#"+"\n"+"#"*50)
		print(" "*((50-len(self.name))/2)+self.name+" "*((50-len(self.name))/2)+"\n")
        	for i in range(len(self.choices)):
            		print(str(i+1)+". "+self.choices[str(i+1)])

    	def user_input(self):
        	while str(self.user_ch) not in self.choices.keys():
            		print('-'*50+"\nVeuillez entrer un nombre parmi {}".format(', '.join(str(i+1) for i in range(len(self.choices)))))
			self.user_ch = input("Choix utilisateur : ")
		return int(self.user_ch)

	def do_method(self):
		self.fcts[int(self.user_ch)-1]()

	def quit_menu(self):
		return
        
class LibMenu(Menu):
	def __init__(self, lib):
		Menu.__init__(self, lib)
		self.name = "Choix de l'echantillon"
		self.choices = dict()
		for i in range(len(lib.dbs)):
			self.choices[str(i+1)] = lib.dbs[i].name
		self.choices[str(i+2)] = "Retour"
		self.choices[str(i+3)] = "Quitter"

class SelectMenu(Menu):
	def __init__(self, lib):
		Menu.__init__(self, lib)
		self.name "Outil de selection"
		self.choices = {"1":"Contrainte simple",
				"2":"Bloc OU",
				"3":"Bloc ET",
				"4":"Retour",
				"5":"Quitter"}
		self.filter = Filter(lib.bds[0])
		self.fcts = [self.filter.add_ctr,
				self.filter.add_ctr,
				self.filter.add_ctr]

class MainMenu(Menu):
	def __init__(self, lib):
        	Menu.__init__(self, lib)
		self.name = "Menu principal"
        	self.choices = {"1":"Visualiser les donnees",
                        	"2":"Creer une sous-population",
                        	"3":"Traitement statistique",
                        	"4":"Modifier une base",
                        	"5":"Quitter"}
		self.fcts = [self.show_bdd]

	def show_bdd(self):
		lib_menu = LibMenu(lib)
		lib_menu.disp_menu()
		self.lib.dbs[lib_menu.user_input()-1].disp_bdd()

	def add_ech(self):
		

lib = Library()
lib.add_db(BaseDeDonnees("vinData.json"))
main_menu = MainMenu(lib)
main_menu.disp_menu()
main_menu.user_input()
main_menu.do_method()
