import json

class BaseDeDonnees:
	def __init__(self, fichier):
		with open(fichier, "r") as fd:
			self.data = json.load(fd)
		self.vars = self.data[0].keys()
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

class Filtre:
	def __init__(self, bdd):
		self.varlist = bdd.vars
		self.oplist = ['<', '>', '==', '!=']
		self.ctrs = list()
	def __str__(self):
		ret = "Selection des donnees telles que : " + str(self.ctrs[k])


def add_ctr(bdd, ctrs):
	print("##########################\n--- OUTIL DE SELECTION ---\n##########################")
	bl = input("1.Contrainte simple\n2.Bloc OU\n3.Bloc ET\n4.Quitter\n\nChoix utilisateur : ")
	if (bl == 2):
		ctrs = add_ctr(bdd, ctrs)
		ctrs = add_ctr(bdd, ctrs)
		ctrs.append("ou")
	elif (bl == 3):
		add_ctr(bdd, ctrs)
		add_ctr(bdd, ctrs)
		ctrs.append("et")
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
		ctr = Contrainte(bdd.data[0].keys()[vect[0]], vect[1], vect[2])
		ctrs.append(ctr)
	return (ctrs)

def filter_apply(bdd, ctrs):
	pile = list()
	for item in range(len(ctrs)):
		if ctrs[item].__class__.__name__ == "Contrainte":
			print("bite")
			res = []
			for i in range(len(bdd.data)):
				if eval(str(bdd.data[i][ctrs[item].var])+ctrs[item].op+str(ctrs[item].val)):   
					res.append(i)
			pile.append(res)
		if (ctrs[item] == "ou"):
			for i in pile[1]:
				if i not in pile[0]:
					pile[0].append(i)
					print(i)
			del pile[1]
		elif (ctrs[item] == "et"):
			for i in pile[1]:
				if i not in pile[0]:
					pile[0].remove(i)
			del pile[1]
	return (sorted(pile[0]))

bdd = BaseDeDonnees("vinData.json")
ctrs = add_ctr(bdd, list())
for item in range(len(ctrs)):
	print(ctrs[item])
bdd.disp_obs(filter_apply(bdd, ctrs))
