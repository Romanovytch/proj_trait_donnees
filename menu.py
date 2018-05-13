from db import Library, BaseDeDonnees
import stat_descritptive as statd

class Menu:
    def __init__(self, comment = ""):
        self.choices = {}
        self.fcts = []
        self.user_ch = 0
        self.user_choice = ""
        self.name = "Menu"
        self.comment = comment
        self.quit = False
        
    def disp_menu(self):
        print ("\n"*100)
        print("#"*50+"\n"+"#"+" "*22+"MENU"+" "*22+"#"+"\n"+"#"*50)
        print(" "*int(((50-len(self.name))/2))+self.name+" "*int(((50-len(self.name))/2))+"\n")
        if self.comment != "":
            print('>>> '+self.comment+' <<<\n\n')
        for i in range(len(self.choices)):
            if (i == (len(self.choices) - 1)):
                print('')
            print(str(i+1)+". "+self.choices[str(i+1)])

    def user_input(self):
        self.user_ch = 0
        while str(self.user_ch) not in self.choices.keys():
            print('-'*50+"\nVeuillez entrer un nombre parmi {}".format(', '.join(str(i+1) for i in range(len(self.choices)))))
            self.user_ch = input("Choix utilisateur : ")
        return int(self.user_ch)

    def do_method(self):
        self.fcts[int(self.user_ch)-1]()
        
    def start(self):
        while self.quit == False:
            self.disp_menu()
            self.user_input()
            self.do_method()
        
    def get_choice(self):
        self.user_choice = self.choices[self.user_ch]

    def quit_menu(self):
        self.quit = True
        
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
    def __init__(self, filt, comment = ""):
        Menu.__init__(self, comment)
        self.name = "Menu de selection"
        self.choices = dict()
        self.filt = filt
        self.choices = {"1":"Contrainte simple",
                        "2":"Bloc OU",
                        "3":"Bloc ET",
                        "4":"Retour"}
        self.fcts = [self.filt.simple_ctr,
                     self.or_block,
                     self.and_block,
                     self.quit_menu]
                     
    def start(self):
        while (self.quit == False) & (self.filt.success == 0):
            self.disp_menu()
            self.filt.disp_selection()
            self.user_input()
            self.do_method()
            
    def and_block(self):
        self.filt.add_str(" et ")
        ctr1 = SelectMenu(self.filt, "Choisissez un critere pour la contrainte en violet")
        ctr1.start()
        self.filt.success = 0
        ctr2 = SelectMenu(self.filt, "Choisissez un critere pour la contrainte en violet")
        ctr2.start()
        self.filt.ctrs.append("and")
        
    def or_block(self):
        self.filt.add_str(" ou ")
        ctr1 = SelectMenu(self.filt, "Choisissez un critere pour la contrainte en violet")
        ctr1.start()
        self.filt.success = 0
        ctr2 = SelectMenu(self.filt, "Choisissez un critere pour la contrainte en violet")
        ctr2.start()
        self.filt.ctrs.append("or")
                        
class VarMenu(Menu):
    def __init__(self, bdd):
        Menu.__init__(self)
        self.name = "Choix de la variable"
        self.choices = dict()
        for i in range(len(bdd.vars)):
            self.choices[str(i+1)] = bdd.vars[i]
        self.choices[str(i+2)] = "Retour"
        for i in range(len(bdd.vars)):
            self.fcts.append(self.get_choice)
        self.fcts.append(self.quit_menu)
        
    def start(self, filt):
        while self.quit == False:
            self.disp_menu()
            self.user_input()
            self.do_method()
            if self.quit == False:
                op_menu = OpMenu()
                self.quit = op_menu.start(filt, self.user_choice)
        
class OpMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.name = "Choix de l'operateur de comparaison"
        self.choices = dict()
        self.op = ['<', '>', '==', '!=']
        for i in range(len(self.op)):
            self.choices[str(i+1)] = self.op[i]
        self.choices[str(i+2)] = "Retour"
        for i in range(len(self.op)):
            self.fcts.append(self.get_choice)
        self.fcts.append(self.quit_menu)
        
    def start(self, filt, var):
        while self.quit == False:
            self.disp_menu()
            self.user_input()
            self.do_method()
            if self.quit == False:
                val_menu = ValMenu("Appuyez sur entree pour revenir en arriere")
                self.quit = val_menu.start(filt, var, self.user_choice)
            else:
                return False
        
class ValMenu(Menu):
    def __init__(self, comment = ""):
        Menu.__init__(self, comment)
        self.name = "Quelle valeur ?"
        self.choices = dict()

    def user_input(self):
        return input("Entrez une valeur : ")
        
    def start(self, filt, var, op):
        self.disp_menu()
        val = self.user_input()
        if val != "":
            filt.ctrs.append(Contrainte(var, op, val))
            print(var+op+val)
            input()
            filt.add_str(Contrainte(var, op, val))
            filt.success = True
            return True
        return False
            

class NameMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.name = "Nommer l'echantillon"
        self.choices = dict()

    def user_input(self):
        return input("Entrez un nom pour l'echantillon : ")
        
    def start(self):
        self.disp_menu()
        return self.user_input()

        
class StatDescrMenu(Menu):
    def __init__(self, lib):
        Menu.__init__(self)
        self.name = "Resume statistique"
        self.choices = {"1":"Ajout variable",
                        "2":"Valider",
                        "3":"Retour"}
        self.varlist = []
        self.fcts = [self.add_var,
                     self.validate,
                     self.quit_menu]
        self.lib = lib
        
    def start(self):
        while self.quit != True:
            self.disp_menu()
            print(self.varlist)
            self.user_input()
            self.do_method()
        
    def add_var(self):
        vm = VarMenu(lib.dbs[0])
        vm.disp_menu()
        vm.user_input()
        if int(vm.user_ch) <= len(self.lib.dbs[0].vars):
            vm.get_choice()
            self.varlist.append(vm.user_choice)

    def validate(self):
        statd.StatDescr(lib.dbs[0], self.varlist).stat_summary()
        self.quit = True

                    
class StatMenu(Menu):
    def __init__(self, lib):
        Menu.__init__(self)
        self.name = "Traitement statistique"
        self.choices = {"1":"Resume statistique (moyenne, mediane, ecart-type)",
                        "2":"Boxplots",
                        "3":"Tests statistiques",
                        "4":"Retour"}
        self.fcts = [self.stat_descr,
                     self.stat_tests,
                     self.stat_boxplots,
                     self.quit_menu]
        self.lib = lib
                     
    def stat_descr(self):
        StatDescrMenu(self.lib).start()
        
    def stat_boxplots(self):
        return
        
    def stat_tests(self):
        return

        
class MainMenu(Menu):
    def __init__(self, lib):
        Menu.__init__(self)
        self.name = "Menu principal"
        self.choices = {"1":"Visualiser les donnees",
                        "2":"Creer une sous-population",
                        "3":"Traitement statistique",
                        "4":"Modifier une base",
                        "5":"Quitter"}
        self.fcts = [self.show_bdd,
                     self.create_pop,
                     self.stat,
                     self.modify_db,
                     self.quit_menu]
        self.lib = lib

    def show_bdd(self):
        lib_menu = LibMenu(lib)
        lib_menu.disp_menu()
        self.lib.dbs[lib_menu.user_input()-1].disp_bdd()

    def create_pop(self):
        fil = Filter(lib.dbs[0])
        if len(fil.ctrs) != 0:
            self.lib.add_db(self.lib.create_db(fil.ech_name, fil.apply_filter()))
        
    def stat(self):
        StatMenu(lib).start()
        
    def modify_db(self):
        return
		
class Contrainte:
    def __init__(self, var, op, val):
        self.var = var
        self.op = op
        self.val = val
	
    def __str__(self):
        return (self.var + self.op + str(self.val))

class Filter:
    def __init__(self, bdd):
        self.bdd = bdd
        self.oplist = ['<', '>', '==', '!=']
        self.ctrs = list()
        self.select_str = ["''"]
        self.success = 0
        self.ech_name = NameMenu().start()
        sm = SelectMenu(self, "Choisissez un critere pour la contrainte en violet")
        sm.disp_menu()
        self.disp_selection()
        sm.user_input()
        sm.do_method()

    def add_str(self, elem):
        if "''" in self.select_str:
            index = self.select_str.index("''")
            self.select_str.remove("''")
        else:
            index = 0
        if type(elem) == str:
            self.select_str.insert(index, "( ")
            self.select_str.insert(index+1, "''")
            self.select_str.insert(index+2, elem)
            self.select_str.insert(index+3, "''")
            self.select_str.insert(index+4, " )")
        else:
            self.select_str.insert(index, str(elem))

    def disp_selection(self):
        sel_str = "\nSelection des donnees telles que : "
        current_ctr_index = self.select_str.index("''")
        for i in range(len(self.select_str)):
            if i == current_ctr_index:
                sel_str += '\x1b[35m\x1b[1m' + '[CONTRAINTE]' + '\x1b[0m'
            elif self.select_str[i] == "''":
                sel_str += '[CONTRAINTE]'
            else:
                sel_str += self.select_str[i]
        sel_str += '\n'
        print(sel_str)
        
    def add_ctr(self):
        sm = SelectMenu(self, "Choisissez un critere pour la contrainte en violet")
        sm.start()

    def simple_ctr(self):
        varm = VarMenu(self.bdd)
        varm.start(self)
 
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
main_menu.start()
