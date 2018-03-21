from Tkinter import *

class Interface(Frame):
	def __init__(self, fenetre, **kwargs):
		Frame.__init__(self, fenetre, **kwargs)
		self.pack(fill=BOTH)
		self.b_disp = Button(fenetre, text="Visualiser les donnees", command=fenetre.quit).pack()
		self.b_stat = Button(fenetre, text="Traitement statistiques", command=fenetre.quit).pack()
		self.b_mdb = Button(fenetre, text="Modifier donnees", command=fenetre.quit).pack()
		self.b_quit = Button(fenetre, text="Quitter", command=fenetre.quit).pack()

fenetre = Tk()

label = Label(fenetre, text="Hello world!")
label.pack()


b_disp.pack()
b_stat.pack()
b_mdb.pack()
b_quit.pack()

fenetre.mainloop()
