# -*- coding: utf-8 -*-
"""
Created on Sun Apr  1 14:02:53 2018

@author: id1157
"""

import numpy as np
import copy
import sys

from random import randint

class Cluster:
    def __init__(self,bdd): #la classe Cluster prend en attribut la liste de vins de la base de donnée
        self.data=bdd.data
        self.bdd = bdd
        print("\nVeuillez patienter")
        print('[', end='', flush=True)
    
    def centr_red(self): #renvoie une copie de la base de donnée centrée réduite pour chaque valeur
        ctrd=copy.deepcopy(self)
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
   
    def progress(self, count, total, status=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        percents = round(100.0 * count / float(total), 1)
        bar = ('\x1b[32m\x1b[1m' + '\u25A0' + '\x1b[0m') * filled_len + '-' * (bar_len - filled_len)
        sys.stdout.write('\r[%s] %s%s ...%s\r' % (bar, percents, '%', status))
        sys.stdout.flush() 
        
    def clustering(self,p): #algorithme des K-means
        ctrd=self.centr_red()
        barys_initiaux=ctrd.barycentres_aleatoires(p)
        barycentres=[ctrd.data[i] for i in barys_initiaux]
        groupes=ctrd.regroupement(barycentres)
        barycentres=ctrd.barycentres_groupes(groupes)
        for i in range(20):
            self.progress(i, 20, "Clustering en cours")
            copy=list(groupes)
            groupes=ctrd.regroupement(barycentres)
            barycentres=ctrd.barycentres_groupes(groupes)
            if ctrd.fin_iteration(groupes,copy)==True:
                final=[]
                barys_non_centred=[]
                for groupe in groupes:
                    a=[vin['wine identity'] for vin in groupe]
                    a.remove(a[0])
                    final.append(a)
                    bary_non_centred=self.barycentrage_groupe([self.data[k-1] for k in a])
                    barys_non_centred.append(bary_non_centred)
                self.display_clustering(final,barys_non_centred)
        final=[]
        barys_non_centred=[]
        for groupe in groupes:
            a=[vin['wine identity'] for vin in groupe]
            a.remove(a[0])
            final.append(a)
            bary_non_centred=self.barycentrage_groupe([self.data[k-1] for k in a])
            barys_non_centred.append(bary_non_centred)
        self.display_clustering(final, barys_non_centred)

    def display_clustering(self, groups, barycentres):
        for i in range(len(groups)):
            print("\n\nGroupe "+str(i+1)+" :\n"+"#"*10+" "+str(len(groups[i]))+ " vins.")
            print("#"*10+" Vin representatif du groupe : ")
            print(barycentres[i])
        input("Appuyez sur entree pour revenir au menu")
