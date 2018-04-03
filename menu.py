import os

class Menu:
    def __init__(self):
        self.choices = {}
        self.user_ch = 0
        
    def disp_menu(self):
        print("#"*50+"\n"+"#"+" "*22+"MENU"+" "*22+"#"+"\n"+"#"*50)
        for i in range(len(self.choices)):
            print(str(i+1)+". "+self.choices[str(i+1)])

    def user_input(self):
        while self.user_ch not in self.choices.keys():
            print('-'*50+"\nVeuillez entrer un nombre parmi {}".format(
                  ', '.join(str(i+1) for i in range(len(self.choices)))))
            self.user_ch = input("Choix utilisateur : ")
        
        
class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self)
        self.choices = {"1":"Visualiser les donnees",
                        "2":"Creer une sous-population",
                        "3":"Traitement statistique",
                        "4":"Modifier une base",
                        "5":"Quitter"}

main_menu = MainMenu()
main_menu.disp_menu()
main_menu.user_input()
