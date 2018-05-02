from db import Library, BaseDeDonnees

class Menu:
    def __init__(self):
        self.choices = {}
        self.user_ch = 0
        self.name = "Menu"
        
    def disp_menu(self):
        print ("\n"*100)
        print("#"*50+"\n"+"#"+" "*22+"MENU"+" "*22+"#"+"\n"+"#"*50)
        print(" "*int(((50-len(self.name))/2))+self.name+" "*int(((50-len(self.name))/2))+"\n")
        for i in range(len(self.choices)):
            print(str(i+1)+". "+self.choices[str(i+1)])

    def user_input(self):
        self.user_ch = 0
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
        Menu.__init__(self)
        self.name = "Choix de l'echantillon"
        self.choices = dict()
        for i in range(len(lib.dbs)):
            self.choices[str(i+1)] = lib.dbs[i].name
        self.choices[str(i+2)] = "Retour"
        self.choices[str(i+3)] = "Quitter"

class SelectMenu(Menu):
    def __init__(self, filt):
        Menu.__init__(self)
        self.name = "Menu de selection"
        self.choices = dict()
        self.filt = filt
        self.choices = {"1":"Ajouter contrainte simple",
                        "2":"Ajouter un bloc OU",
                        "3":"Ajouter un bloc ET",
                        "4":"Quitter"}
        self.fcts = [self.filt.simple_ctr,
                     self.filt.or_block,
                     self.filt.and_block]
                        
class VarMenu(Menu):
    def __init__(self, bdd):
        Menu.__init__(self)
        self.name = "Choix de la variable"
        self.choices = dict()
        for i in range(len(bdd.vars)):
            self.choices[str(i+1)] = bdd.vars[i]
        self.choices[str(i+2)] = "Retour"
        self.choices[str(i+3)] = "Quitter"
        
class OpMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.name = "Choix de l'operateur de comparaison"
        self.choices = dict()
        self.op = ['<', '>', '==', '!=']
        for i in range(len(self.op)):
            self.choices[str(i+1)] = self.op[i]
        self.choices[str(i+2)] = "Retour"
        self.choices[str(i+3)] = "Quitter"
        
class ValMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.name = "Quelle valeur ?"
        self.choices = dict()

    def user_input(self):
        return input("Entrez une valeur : ")

class NameMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.name = "Nommer l'echantillon"
        self.choices = dict()

    def user_input(self):
        return input("Entrez un nom pour l'echantillon : ")
        
class MainMenu(Menu):
    def __init__(self, lib):
        Menu.__init__(self)
        self.name = "Menu principal"
        self.choices = {"1":"Visualiser les donnees",
                        "2":"Creer une sous-population",
                        "3":"Traitement statistique",
                        "4":"Modifier une base",
                        "5":"Quitter"}
        self.fcts = [self.show_bdd, self.create_pop]
        self.lib = lib

    def show_bdd(self):
        lib_menu = LibMenu(lib)
        lib_menu.disp_menu()
        self.lib.dbs[lib_menu.user_input()-1].disp_bdd()

    def create_pop(self):
        nm = NameMenu()
        nm.disp_menu()
        name = nm.user_input()
        fil = Filter(lib.dbs[0])
        fil.add_ctr()
        self.lib.add_db(self.lib.create_db(name, fil.apply_filter()))
        self.lib.dbs[1].disp_bdd()
        

		
class Contrainte:
    def __init__(self, var, op, val):
        self.var = var
        self.op = op
        self.val = val
	
    def __str__(self):
        return (self.var + self.op + str(self.val))

class Filter:
    def __init__(self, bdd):
        self.varlist = bdd.vars
        self.oplist = ['<', '>', '==', '!=']
        self.ctrs = list()
        self.bdd = bdd

    def add_ctr(self):
        sm = SelectMenu(self)
        sm.disp_menu()
        sm.user_input()
        sm.do_method()
    
    def and_block(self):
        self.add_ctr()
        self.simple_ctr()
        self.simple_ctr()
        self.ctrs.append("and")
        
    def or_block(self):
        self.add_ctr()
        self.simple_ctr()
        self.simple_ctr()
        self.ctrs.append("or")
        
    def simple_ctr(self):
        varm = VarMenu(self.bdd)
        varm.disp_menu()
        varm.user_input()
        var = varm.get_choice()
        opm = OpMenu()
        opm.disp_menu()
        opm.user_input()
        op = opm.get_choice()
        valm = ValMenu()
        valm.disp_menu()
        val = valm.user_input()
        self.ctrs.append(Contrainte(var, op, val))
 
    def apply_filter(self):
        pile = list()
        for item in range(len(self.ctrs)):
            if self.ctrs[item].__class__.__name__ == "Contrainte":
                res = []
                for i in range(len(self.bdd.data)):
                    if eval(str(self.bdd.data[i][self.ctrs[item].var])+self.ctrs[item].op+str(self.ctrs[item].val)):   
                        res.append(i)
                        pile.append(res)
            if (self.ctrs[item] == "ou"):
                for i in pile[1]:
                    if i not in pile[0]:
                        pile[0].append(i)
                        print(i)
                del pile[1]
            elif (self.ctrs[item] == "et"):
                et_res = list()
                for i in pile[0]:
                    if i in pile[1]:
                        et_res.append(i)
                        pile[0] = et_res
                del pile[1]
        print(pile[0])
        return (sorted(pile[0]))        
        
lib = Library()
lib.add_db(BaseDeDonnees("vinData.json"))
main_menu = MainMenu(lib)
while main_menu.user_ch != 5:
    main_menu.disp_menu()
    main_menu.user_input()
    main_menu.do_method()
