# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 14:02:53 2018

@author: id1157
"""

import numpy as np
import copy

from random import randint

class Cluster:
    def __init__(self,bdd): #la classe Cluster prend en attribut la liste de vins de la base de donnée
        self.data=bdd.data
    
    def centr_red(self): #renvoie une copie de la base de donnée centrée réduite pour chaque valeur
        ctrd=copy.copy(self)
        for var in ctrd.data[0].keys():
            if var!='wine identity' and var!='type':
                mean=np.mean([vin[var] for vin in ctrd.data])
                sd=np.std([vin[var] for vin in ctrd.data])
                for vin in ctrd.data:
                    vin[var]=(vin[var]-mean)/sd
        return ctrd
                
    def distance(self,vin1,vin2): #calcule la distance euclidienne de vin1 à vin2
        d=0
        for i in vin1.keys():
            if i!='wine identity' and i!='type':
                d+=(vin1[i]-vin2[i])**2
        d=np.sqrt(d)
        return d
    
    def barycentres_aleatoires(self,p):  #choisit p barycentres aléatoirement parmi les vins de la base
        barys_initiaux=[]
        a=randint(0,len(self.data)-1)
        for i in range(p):
            while a in barys_initiaux:
                  a=randint(0,len(self.data)-1)
            barys_initiaux.append(a)
        return barys_initiaux
        
    def grp_vin(self, vin, barycentres): #affecte le vin à un groupe, ie au barycentre le plus proche de ce vin
        distances = []
        for bary in barycentres:
            distances.append(self.distance(self.data[vin],bary))
        return distances.index(min(distances))
    
    def regroupement(self,barycentres): #retourne les groupes de vin après affectation de chaque vin à un groupe
        groupes=[[bary] for bary in barycentres]
        for vin in range(len(self.data)):
            i=self.grp_vin(vin,barycentres)
            groupes[i].append(self.data[vin])
        return groupes

    def barycentrage_groupe(self,groupe): #rebarycentre le groupe à partir de tous les vins du groupe
        G={key:0 for key in self.data[0].keys()}
        for var in self.data[0].keys():
            for vin in groupe:
                if var!='wine identity' and var!='type':
                    G[var]+=vin[var]
            G[var]=G[var]/len(groupe)
        return G
    
    def barycentres_groupes(self,groupes): #renvoie la liste des groupes barycentrés
        L=[]
        for groupe in groupes:
            L.append(self.barycentrage_groupe(groupe))
        return L
    
    
    def fin_iteration(self,groupes,copy): #vérifie si l'algorithme des K-means converge, en regardant si les groupes sont restés les mêmes d'une itération à l'autre
        for gr in range(len(groupes)):
            for vin in groupes[gr]:
                if vin not in copy[gr]:
                        return False
        return True
        
    def clustering(self,p): #algorithme des K-means
        ctrd=self.centr_red()
        barys_initiaux=ctrd.barycentres_aleatoires(p)
        barycentres=[ctrd.data[i] for i in barys_initiaux]
        groupes=ctrd.regroupement(barycentres)
        barycentres=ctrd.barycentres_groupes(groupes)
        for i in range(20):
            copy=list(groupes)
            groupes=ctrd.regroupement(barycentres)
            barycentres=ctrd.barycentres_groupes(groupes)
            if ctrd.fin_iteration(groupes,copy)==True:
                final = [[vin['wine identity'] for vin in groupe] for groupe in groupes]
                self.display_clustering(final)
        final = [[vin['wine identity'] for vin in groupe] for groupe in groupes]
        self.display_clustering(final)

    def display_clustering(self, groups):
        for i in range(len(groups)):
            print("Groupe "+str(i+1)+" :\n#Vins : {}".format(', '.join(str(index) for index in groups[i])))
        input("Appuyez sur entree pour revenir au menu")
            
        