import json
import Tkinter as tk

class BaseDeDonnees:
	def __init__(self, fichier):
		with open(fichier, "r") as fd:
			self.data = json.load(fd)
		self.vars = self.data[0].keys()

	def disp_obs(self, index):
		s = ""
		s = s+('{:6}|'.format("Obs")+''.join('{:4}|'.format(var) for var in self.vars))+'\n'
		for i in index:
			s = s + ('{:6}|'.format(str(i))+''.join('{:4}|'.format(str(self.data[i][k])[:7]+' '*(len(k)-len(str(self.data[i][k])))) for k in self.vars))
			s = s + '\n'
		return s
	
	def disp_bdd(self):
		return self.disp_obs(range(len(self.data)))
	
	def del_obs(self, index):
		for i in index:
			del self.data[i]

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self._frame = StartPage(master=self.container, controller=self)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(master=self.container, controller=self)
        self._frame.destroy()
        self._frame = new_frame


class StartPage(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        start_label = tk.Label(self, text="This is the start page")
        page_1_button = tk.Button(self, text="Open page one",
                                  command=lambda: controller.switch_frame(PageOne))
        page_2_button = tk.Button(self, text="Open page two",
                                  command=lambda: controller.switch_frame(PageTwo))
        start_label.pack(side="top", fill="x", pady=10)
        page_1_button.pack()
        page_2_button.pack()
        self.pack()


class Table(tk.Frame):
	def __init__(self, master, bdd, rows, columns):
		tk.Frame.__init__(self, master, background="black")
		self.widgets = []
		for column in range(columns):
			label = tk.Label(self, text=bdd.vars[column])
			label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
		for row in range(rows):
			current_row = []
			for column in range(columns):
				label = tk.Label(self, text=bdd.data[row][bdd.vars[column]])
				label.grid(row=row+1, column=column, sticky="nsew", padx=1, pady=1)
				current_row.append(label)
			self.widgets.append(current_row)
		for column in range(columns):
			self.grid_columnconfigure(column, weight=1)

	def set(self, row, column, value):
		widget = self.widgets[row][column]
		widget.configure(text=value)

class PageOne(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller
	bdd = BaseDeDonnees("vinData.json")
	table = Table(self, bdd, 10, len(bdd.vars))
	title = tk.Label(self, text="Base de donnees des vins :")
	title.pack()
	table.pack(side="top", fill="x")
        start_button = tk.Button(self, text="Return to start page", command=lambda: controller.switch_frame(StartPage))
        start_button.pack()
        self.pack()


class PageTwo(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.controller = controller

        page_2_label = tk.Label(self, text="This is page two")
        start_button = tk.Button(self, text="Return to start page",
                                 command=lambda: controller.switch_frame(StartPage))
        page_2_label.pack(side="top", fill="x", pady=10)
        start_button.pack()
        self.pack()


if __name__ == "__main__":
    	app = SampleApp()
    	app.mainloop()
