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
        print ("\n"*100)
        print('{:6}|'.format("Obs")+''.join('{:4}|'.format(var) for var in list(self.data[0].keys())))
        entry = ""
        show_all = False
        for i in range(1,len(index)):
            if show_all == False:
                if (i % 10) == 0:
                    entry = ""
                    while entry not in ["A","S"]:
                        entry = input("\nEntrez S pour voir les dix suivantes ou A pour tout afficher : ")
                        if entry == "A":
                            show_all = True
                        else:
                            print('{:6}|'.format("Obs")+''.join('{:4}|'.format(var) for var in list(self.data[0].keys())))
            print('\n{:6}|'.format(str(i))+''.join('{:4}|'.format(str(self.data[i][k])[:7]+' '*(len(k)-len(str(self.data[i][k])))) for k in list(self.data[0].keys())))
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
