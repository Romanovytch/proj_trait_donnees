# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 09:55:56 2018

@author: id1157
"""
import numpy as np
import matplotlib.pyplot as plt

class StatDescr:
    def __init__(self, bdd, variables): #la classe StatDescr prend en attribut la base de donnée et les variables sur lesquelles on soouhaite travailler
        self.bdd=bdd
        self.variables=variables
        self.disp = [{"Moyenne":"", "Mediane":"", "Ecart-type":""}]
        self.stats = ["Moyenne", "Mediane", "Ecart-type"]
    
    def stat_mean(self): #calcule la moyenne de chaque variable
        moyenne=[]
        for var in self.variables:
            moyenne.append(np.mean([vin[var] for vin in self.bdd.data]))
        return moyenne
        
    def stat_med(self): #calcule la médiane de chaque variable
        mediane=[]
        for var in self.variables:
           mediane.append(np.median([vin[var] for vin in self.bdd.data])) 
        return mediane
           
    def stat_sd(self): #calcule l'écart-type de chaque variable
        sd=[]
        for var in self.variables:
           sd.append(np.std([vin[var] for vin in self.bdd.data]))
        return sd
        
    def boxplot(self): #affiche la boîte à moustaches de chaque variable
        data=[]
        for i in self.variables:
            data_i=[]
            for j in range (len(self.bdd.data)):
                data_i.append(self.bdd.data[j][i])
            data.append(data_i)
        plt.boxplot(data) 
    
    def stat_summary(self): #renvoie les statistiques de chaque variable et sa boîte à moustaches
        print('\n'*100)
        print("Resume statistiques (moyenne, mediane et ecart-type)"+"\n\n")
        mean = self.stat_mean()
        med = self.stat_med()
        sd = self.stat_sd()
        stat = dict()
        print('{:20}|'.format("VARIABLE")+''.join('{:10}|'.format(var) for var in self.stats))
        print('-'*54)
        for i in range(len(self.variables)):
            stat["Moyenne"] = mean[i]
            stat["Mediane"] = med[i]
            stat["Ecart-type"] = sd[i]
            print('{:20}|'.format(self.variables[i])+''.join('{:10}|'.format(str(stat[k])[:7]+' '*(len(k)-len(str(stat[k])))) for k in self.stats))
        self.boxplot()
        input("Appuyez sur entree pour revenir au menu stat")