import json
import menu

class BaseDeDonnees:
    def __init__(self, fichier, name = "Base complete"):
        with open(fichier, "r") as fd:
            self.data = json.load(fd)
            self.vars = self.data[0].keys()
            self.name = name

    def disp_obs(self, index):
        print('{:6}|'.format("Obs")+''.join('{:4}|'.format(var) for var in self.vars))
        for i in index:
            print('{:6}|'.format(str(i))+''.join('{:4}|'.format(str(self.data[i][k])[:7]+' '*(len(k)-len(str(self.data[i][k])))) for k in self.vars))
	
    def disp_bdd(self):
        self.disp_obs(range(len(self.data)))
	
    def del_obs(self, index):
        for i in index:
            del self.data[i]
		
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
        sm = menu.SelectMenu()
        sm.disp_menu()
        sm.user_input()
        sm.do_method()
    
    def and_block(self):
        add_ctr()
        simple_ctr()
        simple_ctr()
        ctrs.append("and")
        
    def or_block(self):
        add_ctr()
        simple_ctr()
        simple_ctr()
        ctrs.append("or")
        
    def simple_ctr(self):
        varm = menu.VarMenu()
        varm.disp_menu()
        varm.user_input()
        var = vm.get_choice()
        opm = menu.OperatorMenu()
        opm.disp_menu()
        opm.user_input()
        op = om.get_choice()
        '''valm = menu.ValMenu()
        valm.u_input()
        val = valm.user_ch'''
        self.ctrs.append(Contrainte(self.varlist[var], self.oplist[opm], 42))
 
    def apply_filter(bdd):
        pile = list()
        for item in range(len(self.ctrs)):
            if self.ctrs[item].__class__.__name__ == "Contrainte":
                res = []
                for i in range(len(bdd.data)):
                    if eval(str(bdd.data[i][self.ctrs[item].var])+self.ctrs[item].op+str(self.ctrs[item].val)):   
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
        return (sorted(pile[0]))

class Library:
    def __init__(self):
        self.dbs = []

    def add_db(self, db):
        self.dbs.append(db)
	
    def rm_db(self, index):
        del self.lib[index]

'''def add_ctr(self):
        if choice == 2:
            self.ctrs = self.add_ctr()
            self.ctrs = self.add_ctr()
            self.ctrs.append("ou")
        elif choice == 3:
            self.ctrs = self.add_ctr()
            self.ctrs = self.add_ctr()
            self.ctrs.append("et")
        else:
            vect = list()
            print("\n\n##### Variables :\n")
            for i in range(len(bdd.data[0].keys())):
                print(str(i)+". "+bdd.data[0].keys()[i])	
            vect.append(int(input("\nChoix utilisateur ? : ")))
            print("\n\n##### Conditions :\n")
            op = ['<', '>', '==', '!=']
            for k in range(len(op)):
                print(str(k)+". "+bdd.data[0].keys()[vect[0]]+" "+op[k])
            vect.append(op[int(input("\n\nChoix utilisateur ? : "))])
            vect.append(input("\n\n##### Valeur :\n\nChoix utilisateur : "))
            self.ctr = Contrainte(bdd.data[0].keys()[vect[0]], vect[1], vect[2])
            self.ctrs.append(ctr)
            return self.ctrs'''