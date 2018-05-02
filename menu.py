import os
import db

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
        
    def get_choice(self):
        return self.choices[self.user_ch]

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
        self.name = "Menu de selection"
        self.choices = dict()
        self.choices = {"1":"Ajouter contrainte simple",
                        "2":"Ajouter un bloc OU",
                        "3":"Ajouter un bloc ET",
                        "4":"Quitter"}
        self.fcts = [db.Filter.simple_ctr,
                     db.Filter.or_block,
                     db.Filter.and_block]
                        
class VarMenu(Menu):
    def __init__(self, lib):
        Menu.__init__(self, lib)
        self.name = "Choix de la variable"
        self.choices = dict()
        for i in range(len(lib.dbs[0].vars)):
            self.choices[str(i+1)] = lib.dbs[0].vars[i]
        self.choices[str(i+2)] = "Retour"
        self.choices[str(i+3)] = "Quitter"
        
class OpMenu(Menu):
    def __init__(self, lib, op):
        Menu.__init__(self, lib)
        self.name = "Choix de l'operateur de comparaison"
        self.choices = dict()
        for i in range(len(op)):
            self.choices[str(i+1)] = op[i]
        self.choices[str(i+2)] = "Retour"
        self.choices[str(i+3)] = "Quitter"

class MainMenu(Menu):
    def __init__(self, lib):
        Menu.__init__(self, lib)
        self.name = "Menu principal"
        self.choices = {"1":"Visualiser les donnees",
                        "2":"Creer une sous-population",
                        "3":"Traitement statistique",
                        "4":"Modifier une base",
                        "5":"Quitter"}
        self.fcts = [self.show_bdd, self.create_pop]

    def show_bdd(self):
        lib_menu = LibMenu(lib)
        lib_menu.disp_menu()
        self.lib.dbs[lib_menu.user_input()-1].disp_bdd()

    def create_pop(self):
        fil = db.Filter(lib.dbs[0])
        fil.add_ctr()
        lib.bds[0].disp_bdd(fil.apply_filter())

lib = db.Library()
lib.add_db(db.BaseDeDonnees("vinData.json"))
main_menu = MainMenu(lib)
main_menu.disp_menu()
main_menu.user_input()
main_menu.do_method()
