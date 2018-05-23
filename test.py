# -*- coding: utf-8 -*-
"""
Created on Tue May 15 16:56:27 2018

@author: id1157
"""

import cluster as cl
import unittest

class Test(unittest.TestCase):
    
    def test_length_barys_aleatoires(self,p=10):
        self.assertEqual(p,len(cl.Cluster(cl.BaseDeDonnees('vinData.json')).barycentres_aleatoires(p)))

    def test_unicite_barycentres(self,p=10):
        L=cl.Cluster(cl.BaseDeDonnees('vinData.json')).barycentres_aleatoires(p)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                assert i!=j

    def test_type_regroupement(self,p=10):
        cluster=cl.Cluster(cl.BaseDeDonnees('vinData.json'))
        vin1=cl.BaseDeDonnees('vinData.json').data[0]
        vin2=cl.BaseDeDonnees('vinData.json').data[1]
        d=cluster.distance(vin1,vin2)
        self.assertTrue(d>=0)
        
unittest.main()