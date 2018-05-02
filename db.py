import json

class BaseDeDonnees:
    def __init__(self, fichier = 0, name = "Base complete"):
        if fichier != 0:
            with open(fichier, "r") as fd:
                self.data = json.load(fd)
                self.vars = list(self.data[0].keys())
        else:
            self.data = list(dict())
        self.name = name

    def disp_obs(self, index):
        print('{:6}|'.format("Obs")+''.join('{:4}|'.format(var) for var in list(self.data[0].keys())))
        for i in index:
            print('{:6}|'.format(str(i))+''.join('{:4}|'.format(str(self.data[i][k])[:7]+' '*(len(k)-len(str(self.data[i][k])))) for k in list(self.data[0].keys())))
        input("\n\nAppuyez sur une touche pour revenir au menu :")
	
    def disp_bdd(self):
        self.disp_obs(range(len(self.data)))

    def add_obs(self, obs):
        self.data.append(obs)
        
    def del_obs(self, index):
        for i in index:
            del self.data[i]


class Library:
    def __init__(self):
        self.dbs = []

    def create_db(self, name, index_list):
        new_db = BaseDeDonnees(0, name)
        for i in index_list:
            new_db.add_obs(self.dbs[0].data[i])
        return new_db

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