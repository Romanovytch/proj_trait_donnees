import json

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
		

class Library:
	def __init__(self):
		self.lib = []

	def add_db(self, db):
		self.lib.append(db)
	
	def rm_db(self, index):
		del self.lib[index]

