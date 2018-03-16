import json

class BaseDeDonnees:
	def __init__(self, fichier):
		with open(fichier, "r") as fd:
			self.data = json.load(fd)


def add_ctr(bdd, ctrs):
	print(type(ctrs))
	bl = input("1. Ajouter une contrainte\n2.Bloc OU\n3.Bloc ET\n4.Quitter\n")
	if (bl == 2):
		print("Selection de CTR1 ou CTR2")
		add_ctr(bdd, ctrs)
		add_ctr(bdd, ctrs)
		ctrs.append("ou")
	elif (bl == 3):
		print("Selection de CTR1 et CTR2")
		add_ctr(bdd, ctrs)
		add_ctr(bdd, ctrs)
		ctrs.append("et")
	else:
		print(ctrs)
		ctr = list()
		for k in bdd.data[0].keys():
			print(k)	
		ctr.append(int(input("Quelle var ? : ")))
		ctr.append(input("\n1. >\n2. <\n3. =\n4. !=\nQuelle operation ? : "))
		ctr.append(input("Valeur ? : "))
		ctrs.append(ctr)
		print(ctrs)
	return (ctrs)

bdd = BaseDeDonnees("vinData.json")
ctrs = add_ctr(bdd, list())
print(ctrs)
