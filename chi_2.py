from scipy import misc  
from scipy import stats
import error as err


class test:
    def __init__(self, var_l, var_c, data):
        self.varname1 = var_l #nom de la variable ligne
        self.varname2 = var_c #nom de la variable colonne
        self.data = data #base de données
        self.var2 = [] #liste des modalites colonne
        self.var1 = [] #liste des modalites ligne
        if type(data[0][var_l]) is not str and type(data[0][var_c]) is not str : #on separe les cas de variables quantitatives et qualitatives
            for k in range(0,len(self.quanti_quali()[var_l])-1) :
                self.var1.append(str(self.quanti_quali()[var_l][k]) + ' - ' + str(self.quanti_quali()[var_l][k+1])) #lorsque la variable est quantitaive on cree 4 modalites qui correspondent au 4 intervalles formes par les quartiles
            for j in range(0,len(self.quanti_quali()[var_c])-1) :
                self.var2.append(str(self.quanti_quali()[var_c][j]) + ' - ' + str(self.quanti_quali()[var_c][j+1]))
        elif  type(data[0][var_l]) is not str and type(data[0][var_c]) is str :
            for k in range(0,len(self.quanti_quali()[var_l])-1) :
                self.var1.append(str(self.quanti_quali()[var_l][k]) + ' - ' + str(self.quanti_quali()[var_l][k+1]))
            self.var2 = self.quanti_quali()[var_c] #lorsque la variable est qualitative on ajoute simplement les modalites deja donnees
        elif type(data[0][var_l]) is str and type(data[0][var_c]) is not str :
            for k in range(0,len(self.quanti_quali()[var_c])-1) :
                self.var2.append(str(self.quanti_quali()[var_c][k]) + ' - ' + str(self.quanti_quali()[var_c][k+1]))
            self.var1 = self.quanti_quali()[var_l]
        else :
            self.var1 = self.quanti_quali()[var_l]
            self.var2 = self.quanti_quali()[var_c]
    
    def quanti_quali(self): #cree un dictionnaire des variables quantitatives avec pour valeurs les quartiles et qualitatives avec pour valeurs les modalites
        variable = [self.varname1, self.varname2]
        valeur_quant = {} #dictionnaire des valeurs de chaque variable quantitative
        valeur_qual = {} #dictionnaire des modalites pour chaque variable qualitative
        quartiles = [] #liste des quartiles de la variable quantitative l (2eme boucle)
        var_quart = {} #dictionnaire qui contient en cles les variables et en valeurs les quartiles si quanti et les modalites si quali
        for l in variable:
            if type(self.data[0][l]) != str:
                valeur_quant[l] = []
                for k in self.data:
                    valeur_quant[l].append(k[l])
            else :
                valeur_qual[l]=[]
                for k in self.data:
                    if k[l] not in valeur_qual[l] :
                        valeur_qual[l].append(k[l])
        for l in variable:  
            if type(self.data[0][l]) != str:
                for m in range(0,4): 
                    quartiles.append(str(round((min(valeur_quant[l])+m*(max(valeur_quant[l])-min(valeur_quant[l]))/4),3))) #on peut aussi faire avec les quartiles : np.percentile(valeur_quant[l], m*25
                var_quart[l] = quartiles
                quartiles = [] 
            else :
                var_quart[l]=valeur_qual[l]
        return var_quart


    def cont_obs(self): #creation du tableau des observations
        effectif = 0 #sera incremente pour remplir chaque case du tableau des observations
        array_obs = [['var2|var1'] + self.var1] #premiere ligne du tableau des observations
        if type(self.data[0][self.varname1]) is not str and type(self.data[0][self.varname2]) is not str : # on fait à nouveau les differents cas : qualitatif ou quantitatif
            for k in range(1,len(self.var2)+1):
                array_obs.append([self.var2[k-1]])
                for l in range (1,len(self.var1)+1):
                    for j in self.data:
                        if (j[self.varname1] > float(self.var1[l-1].split(' - ')[0]) and j[self.varname1] < float(self.var1[l-1].split(' - ')[1]) and j[self.varname2] > float(self.var2[k-1].split(' - ')[0]) and j[self.varname2] < float(self.var2[k-1].split(' - ')[1])) :
                            effectif+=1
                    array_obs[k].append(effectif)
                    effectif = 0
        elif type(self.data[0][self.varname1]) is str and type(self.data[0][self.varname2]) is not str :
            for k in range(1,len(self.var2)+1):
                array_obs.append([self.var2[k-1]])
                for l in range (1,len(self.var1)+1):
                    for j in self.data:
                        if (j[self.varname1] is self.var1[l-1] and j[self.varname2] > float(self.var2[k-1].split(' - ')[0]) and j[self.varname2] < float(self.var2[k-1].split(' - ')[1])) :
                            effectif+=1
                    array_obs[k].append(effectif)
                    effectif = 0
        elif type(self.data[0][self.varname1]) is not str and type(self.data[0][self.varname2]) is str :
            for k in range(1,len(self.var2)+1):
                array_obs.append([self.var2[k-1]])
                for l in range (1,len(self.var1)+1):
                    for j in self.data:
                        if (j[self.varname1] > float(self.var1[l-1].split(' - ')[0]) and j[self.varname1] < float(self.var1[l-1].split(' - ')[1]) and j[self.varname2] is self.var2[k-1]) :
                            effectif+=1
                    array_obs[k].append(effectif)
                    effectif = 0
        else :
            for k in range(1,len(self.var2)+1):
                array_obs.append([self.var2[k-1]])
                for l in range (1,len(self.var1)+1):
                    for j in self.data:
                        if (j[self.varname1] is self.var1[l-1] and j[self.varname2] is self.var2[k-1]):
                            effectif +=1
                    array_obs[k].append(effectif)
                    effectif = 0
        return array_obs 
        
    def cont_the(self): #creation du tableau theorique
        obs = test.cont_obs(self)
        array_the = [['var2t|var1t'] + self.var1]
        obs1 = 0
        obs2 = 0
        for l in range (1,len(obs)):
            array_the.append([self.var2[l-1]])
            for c in range (1, len(obs[0])):
                for i in range (1, len(obs)):
                    obs1 += float(obs[i][c])
                for j in range (1, len(obs[0])):
                    obs2 += float(obs[l][j])
                array_the[l].append(obs1*obs2/len(self.data)) 
                obs1 = 0
                obs2 = 0
        return array_the
                                                
    def chi_2(self,risk): #teste si les variables sont dependantes (chi2 calcule < chi2 theorique) ou non (inverse)
        obs = self.cont_obs()
        the = self.cont_the()
        chi_2_val = 0
        n=0
        for i in range (1,len(obs)):
            for j in range (1,len(obs[0])):
                if the[i][j] < 5 :
                    n=1
                if the[i][j] != 0:
                    chi_2_val += ((float(obs[i][j])-float(the[i][j]))**2)/float(the[i][j])
        df = (len(self.var2)-1)*(len(self.var1)-1)
        chi_2_ris = self.chi2_risk(risk,df)
        print("\n> Le khi2 est de : " + str(round(chi_2_val,2))+'\n')
        if n == 1 :
            err.Error("Le chi2 n''est pas fiable car certains effectifs observés sont inférieurs à 5")
        if chi_2_val < chi_2_ris:
            return '> Les variables sont indépendantes avec un degré de confiance ' + str(risk)
        else : 
            return '> Les variables sont dépendantes avec un degré de confiance ' + str(risk)

    def chi2_risk(self, risk, df): #calcul du chi2 theorique
        global alpha, dfreedom
        alpha = risk
        dfreedom = df
        return self.newtons_method(self.f, dfreedom)
            
    def newtons_method(self, f, x, tolerance=0.0001):#méthode de Newton pour le calcul du chi2 theorique
        t = tolerance-1
        while  t < tolerance and misc.derivative(self.f, x) != 0 : 
            x1 = x - self.f(x) / misc.derivative(self.f, x) 
            t = abs(x1 - x)
            x = x1
        return x
        
    def f(self, x): #fonction pour calcul du chi2 theorique
        return 1 - stats.chi2.cdf(x, dfreedom) - alpha