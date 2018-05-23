import stat_descritptive as statd
import cluster as clst
import chi_2 as chisq
import error as err

class Menu:
    '''
    Classe mere Menu gerant l'affichage du menu,
    l'entree utilisateur et l'execution de la fonctionnalite choisie
    '''
    def __init__(self, comment = ""):
        self.choices = {}
        self.fcts = []
        self.user_ch = 0
        self.user_choice = ""
        self.name = "Menu"
        self.comment = comment
        self.quit = False
        
    def disp_menu(self):
        print("\n"*100)
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
        while self.check() == False:
            print('-'*50+"\nVeuillez entrer un nombre parmi {}".format(', '.join(str(i+1) for i in range(len(self.choices)))))
            self.user_ch = input("Choix utilisateur : ")
        return int(self.user_ch)

    def check(self):
        if str(self.user_ch) not in self.choices.keys():
            return False
        
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
    '''
    Menu affichant le choix de la base de donnée
    '''
    def __init__(self, lib):
        Menu.__init__(self)
        self.name = "Choix de l'echantillon"
        self.choices = dict()
        for i in range(len(lib.dbs)):
            self.choices[str(i+1)] = lib.dbs[i].name
            self.fcts.append(self.quit_menu)
        self.choices[str(i+2)] = "Retour"
        self.fcts.append(self.quit_menu)
        
    def start(self):
        while self.quit == False:
            self.disp_menu()
            self.user_input()
            self.do_method()

class SelectMenu(Menu):
    '''
    Menu d'echantillonage
    '''
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
    '''
    Menu de choix de la variable
    '''
    def __init__(self, varlist, comment = "", quali = True, quanti = True):
        Menu.__init__(self, comment)
        self.name = "Choix de la variable"
        self.choices = dict()
        self.varlist = varlist
        self.quali = quali
        self.quanti = quanti
        for i in range(len(varlist)):
            self.choices[str(i+1)] = varlist[i]
        self.choices[str(i+2)] = "Retour"
        for i in range(len(varlist)):
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
            
    def check(self):
        if str(self.user_ch) not in self.choices.keys():
            return False
        else:
            if int(self.user_ch)-1 != len(self.varlist):
                if (self.quali == False) & (self.varlist[int(self.user_ch) - 1] == 'type'):
                    err.Error("Choisissez une variable quantitative").display()
                    return False
                if (self.quanti == False) & (self.varlist[int(self.user_ch) - 1] != 'type'):
                    err.Error("Choisissez une variable qualitative").display()
                    return False
        return True
        
class OpMenu(Menu):
    '''
    Menu de choix de l'opérateur
    '''
    def __init__(self):
        Menu.__init__(self)
        self.name = "Choix de l'operateur de comparaison"
        self.choices = dict()
        self.op = ['<', '>', '==', '!=']
        self.var = ""
        for i in range(len(self.op)):
            self.choices[str(i+1)] = self.op[i]
        self.choices[str(i+2)] = "Retour"
        for i in range(len(self.op)):
            self.fcts.append(self.get_choice)
        self.fcts.append(self.quit_menu)
        
    def start(self, filt, var):
        self.var = var
        while self.quit == False:
            self.disp_menu()
            self.user_input()
            self.do_method()
            if self.quit == False:
                val_menu = ValMenu("Appuyez sur entree pour revenir en arriere")
                self.quit = val_menu.start(filt, var, self.user_choice)
            else:
                return False
    def check(self):
        if str(self.user_ch) not in self.choices.keys():
            return False
        if self.var == 'type':
            if int(self.user_ch) in [1, 2]:
                err.Error("Choisir '==' ou '!=' pour une variable qualitative").display()
                return False
        return True
        
class ValMenu(Menu):
    """
    Menu de choix de la valeur
    """
    def __init__(self, comment = ""):
        Menu.__init__(self, comment)
        self.name = "Quelle valeur ?"
        self.choices = dict()
        self.var = ""

    def user_input(self):
        self.user_ch = input("Entrez une valeur : ")
        while self.check() == False:
            self.user_ch = input("Entrez une valeur : ")
        
    def start(self, filt, var, op):
        self.disp_menu()
        self.var = var
        self.user_input()
        if self.user_ch != "":
            filt.ctrs.append(Contrainte(var, op, self.user_ch))
            filt.add_str(Contrainte(var, op, self.user_ch))
            filt.success = True
            return True
        return False
          
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def check(self):
        if self.var != 'type':
            if self.is_number(self.user_ch) == False:
                err.Error("Veuillez entrer un nombre pour une variable quantitative").display()
                return False
            return True
        else:
            self.user_ch = "'"+ self.user_ch + "'" 
            return True  

class NameMenu(Menu):
    '''
    Menu de choix du nom
    '''
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
    """
    Menu de statistiques descriptives
    """
    def __init__(self, db):
        Menu.__init__(self)
        self.name = "Resume statistique"
        self.choices = {"1":"Ajout variable",
                        "2":"Valider",
                        "3":"Retour"}
        self.varlist = []
        self.fcts = [self.add_var,
                     self.validate,
                     self.quit_menu]
        self.db = db
        
    def start(self):
        while self.quit != True:
            self.disp_menu()
            print("\nVariables choisies : {}".format(''.join(' {},'.format(var) for var in self.varlist)))
            self.user_input()
            self.do_method()
        
    def add_var(self):
        vm = VarMenu(self.db.vars, quali = False)
        vm.disp_menu()
        vm.user_input()
        if int(vm.user_ch) <= len(self.db.vars):
            vm.get_choice()
            self.varlist.append(vm.user_choice)

    def validate(self):
        statd.StatDescr(self.db, self.varlist).stat_summary()
        self.quit = True

                    
class StatMenu(Menu):
    def __init__(self, lib):
        Menu.__init__(self)
        self.name = "Traitement statistique"
        self.choices = {"1":"Resume statistique [var. quantitatives]",
                        "2":"Test de khi2",
                        "3":"Retour"}
        self.fcts = [self.stat_quanti,
                     self.stat_tests,
                     self.quit_menu]
        self.lib = lib
        self.varlist = []
                     
    def stat_quanti(self):
        lib_menu = LibMenu(self.lib)
        lib_menu.start()
        if int(lib_menu.user_ch) <= len(self.lib.dbs):
            StatDescrMenu(self.lib.dbs[int(lib_menu.user_ch) - 1]).start()
        
    def stat_tests(self):
        lib_menu = LibMenu(self.lib)
        lib_menu.start()
        self.varlist = []
        if int(lib_menu.user_ch) <= len(self.lib.dbs):
            for i in range(2):
                vm = VarMenu(self.lib.dbs[0].vars, comment = "Choix de la variable "+str(i+1))
                vm.disp_menu()
                vm.user_input()
                if int(vm.user_ch) <= len(self.lib.dbs[0].vars):
                    vm.get_choice()
                    self.varlist.append(vm.user_choice)
                else:
                    i = 3
            if len(self.varlist) == 2:
                chi2 = chisq.test(self.varlist[0], self.varlist[1], self.lib.dbs[int(lib_menu.user_ch)-1].data)
                print(chi2.chi_2(float(input("Entrez un risque : "))))
                input("Appuyez sur entree pour continuer")

class ClusteringMenu(Menu):
    def __init__(self, lib, comment):
        Menu.__init__(self, comment)
        self.name = "Clustering"
        self.choices = dict()
        self.lib = lib

    def user_input(self):
        ch = 0
        while ch not in [str(i) for i in range(1, 21)]:
            ch = input("Entrez un nombre entre 1 et 20 : ")
        self.user_ch = int(ch)
            
    def start(self):
        self.disp_menu()
        self.user_input()
        clst.Cluster(self.lib.dbs[0]).clustering(self.user_ch)
        
class MainMenu(Menu):
    def __init__(self, lib):
        Menu.__init__(self)
        self.name = "Menu principal"
        self.choices = {"1":"Visualiser les donnees",
                        "2":"Creer une sous-population",
                        "3":"Traitement statistique",
                        "4":"Clustering",
                        "5":"Quitter"}
        self.fcts = [self.show_bdd,
                     self.create_pop,
                     self.stat,
                     self.clustering,
                     self.quit_menu]
        self.lib = lib

    def show_bdd(self):
        lib_menu = LibMenu(self.lib)
        lib_menu.start()
        if int(lib_menu.user_ch) <= len(self.lib.dbs):
            self.lib.dbs[int(lib_menu.user_ch) - 1].disp_bdd()

    def create_pop(self):
        fil = Filter(self.lib.dbs[0])
        if len(fil.ctrs) != 0:
            self.lib.add_db(self.lib.create_db(fil.ech_name, fil.apply_filter()))
        
    def stat(self):
        StatMenu(self.lib).start()

    def clustering(self):
        ClusteringMenu(self.lib, "Combien de groupes ?").start()
    
class Contrainte:
    def __init__(self, var, op, val):
        self.var = var
        self.op = op
        self.val = val
	
    def __str__(self):
        return (self.var + self.op + str(self.val))

class Filter:
    """
    Objet responsable de la creation du sous-echantillon
    méthode NPI
    """
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
        varm = VarMenu(self.bdd.vars)
        varm.start(self)
 
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
        
    def apply_filter(self):
        pile = list()
        for item in range(len(self.ctrs)):
            if self.ctrs[item].__class__.__name__ == "Contrainte":
                res = []
                for i in range(len(self.bdd.data)):
                    if self.is_number(self.bdd.data[i][self.ctrs[item].var]) == False:
                        evaluation = "'"+self.bdd.data[i][self.ctrs[item].var]+"'"+self.ctrs[item].op+self.ctrs[item].val
                    else:
                        evaluation = str(self.bdd.data[i][self.ctrs[item].var])+self.ctrs[item].op+self.ctrs[item].val
                    if eval(evaluation):   
                        res.append(i)
                pile.append(res)
            if (self.ctrs[item] == "or"):
                for i in pile[1]:
                    if i not in pile[0]:
                        pile[0].append(i)
                del pile[1]
            elif (self.ctrs[item] == "and"):
                et_res = list()
                for i in pile[0]:
                    if i in pile[1]:
                        et_res.append(i)
                        pile[0] = et_res
                del pile[1]
        return (sorted(pile[0]))
