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
        self.stats = ["Effectif total", "Moyenne", "Mediane", "Ecart-type", "Minimum", "Maximum", "Q1", "Q3", "D1", "D9"]
        self.stats_fcts = [self.st_eftot, self.st_mean, self.st_med, self.st_sd, self.st_min, self.st_max, self.st_q1, self.st_q3, self.st_dec1, self.st_dec9]
    
    def st_eftot(self, values):
        return len(values)
        
    def st_mean(self, values): #calcule la moyenne de chaque variable
        return np.mean(values)
        
    def st_med(self, values): #calcule la médiane de chaque variable
        return np.median(values)
           
    def st_sd(self, values): #calcule l'écart-type de chaque variable
        return np.std(values)
        
    def st_min(self, values):
        return min(values)
        
    def st_max(self, values):
        return max(values)
        
    def st_q1(self, values):
        return np.percentile(values, 25)
        
    def st_q3(self, values):
        return np.percentile(values, 75)
        
    def st_dec1(self, values):
        return np.percentile(values, 10)
        
    def st_dec9(self, values):
        return np.percentile(values, 90)
        
    def boxplot(self): #affiche la boîte à moustaches de chaque variable
        for i in self.variables:
            data_i=[]
            for j in range (len(self.bdd.data)):
                data_i.append(self.bdd.data[j][i])
            plt.boxplot(data_i)
        print("\nDes boxplots ont ete generes sur des fenetres annexes.")
    
    def stat_summary(self): #renvoie les statistiques de chaque variable et sa boîte à moustaches
        print('\n'*100)
        print("Resume statistiques [var. quantitatives]\n\n")
        stat_data = {stat:[] for stat in self.stats}
        value_list = [[] for var in self.variables]
        for wine in self.bdd.data:
            for i in range(len(self.variables)):
                value_list[i].append(wine[self.variables[i]])
        for i in range(len(self.variables)):
            for stat in range(len(self.stats)):
                stat_data[self.stats[stat]].append(self.stats_fcts[stat](value_list[i]))
        print('{:20}|'.format("VARIABLE")+''.join('{:10}|'.format(var) for var in self.stats))
        print('-'*110)
        for i in range(len(self.variables)):
            print('{:20}|'.format(self.variables[i])+''.join('{:10}|'.format(str(stat_data[k][i])[:7]+' '*(len(k)-len(str(stat_data[k][i])))) for k in self.stats))
        self.boxplot()
        input("Appuyez sur entree pour revenir au menu stat")