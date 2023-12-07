# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 05:56:21 2023

@author: edymn
"""

import threading

import logging
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.DEBUG, format='%(threadName)s: %(message)s')

class FMeanCentral():
    
    def __init__(self,numAgents,P_d,limIter):
        self.numAgents = numAgents
        self.listFi_xi = [pd/numAgents for i in range(numAgents)]
        self.aux_listFi_xi = [pd/numAgents for i in range(numAgents)]
        self.P_d = P_d
        self.flagIter = [False for i in range(numAgents)]
        self.numIter = 0
        self.limIter = limIter
        self.fMean = 1
        
        self.listF_i = [0 for i in range(numAgents)]
        self.listX_i = [0 for i in range(numAgents)]
        
        self.listX_evolve = [[] for i in range(numAgents)]
        self.listFi_evolve = [[] for i in range(numAgents)]
        
    def calculateF_Mean(self):
        self.fMean = 0
        for i in self.listFi_xi:
        
            self.fMean += i
        
        self.fMean = self.fMean/self.P_d        
            
    
    def refreshLists(self,fi,xi,id_agente):
        if (not self.flagIter[id_agente]):
            self.flagIter[id_agente] = True
            self.listF_i[id_agente] = fi
            self.listX_i[id_agente] = xi
            self.aux_listFi_xi[id_agente] = fi*xi
            
    def changeIter(self):
        
        flag_change_iter = True
        for i in self.flagIter:
            flag_change_iter = flag_change_iter and i
            
        if flag_change_iter:
            self.flagIter = [False for i in range(self.numAgents)]
            self.listFi_xi = self.aux_listFi_xi
            self.numIter += 1
            self.calculateF_Mean()
                
    def getFlagIter(self):
        return self.flagIter
    
    def getNumIter(self):
        return self.numIter
    
    def getFlagAgent(self,id_agente):
        return not self.flagIter[id_agente]
    
    def getFmean(self):        
        return self.fMean
    
    def saveEvolution(self,x_evol,fi_evol,id_agente):
        self.listFi_evolve[id_agente] = fi_evol
        self.listX_evolve[id_agente] = x_evol
    
    def getListsX_evol(self):
        return self.listX_evolve
    
    def getListsFi_evolve(self):
        return self.listFi_evolve
        
        

class AgentP2P():
    
    def __init__(self,a,b,c,P_d,ID,numAgents):
        
        self.a = a
        self.b = b
        self.c = c
        self.x_k = (P_d/numAgents) + 100 
        self.p = self.x_k
        self.p_evulution = [self.p]  
        self.fi_evolution = [self.f_i()]
        self.f_mean = 1
        self.P_d = P_d
        self.numIter = 0
        self.ID = ID
        self.alpha = 0.001
        
        
    def f_i(self):
        
        fi = -(self.b + 2*(self.c*self.p))  + 2e3
        
        return fi
    
    def X_k(self):        
        
        #self.x_k = self.p*(self.f_i()/self.f_mean)
        self.x_k = self.p + self.alpha*self.p*(self.f_i()-self.f_mean)
        self.p = self.x_k
        self.p_evulution.append(self.x_k)        
    
    def calculateXk(self):
        
        self.X_k()
        self.numIter += 1
    
    def getFi(self):     
        self.fi_evolution.append(self.f_i())
        return self.f_i()
    
    def setF_mean(self, f_mean):
        self.f_mean = f_mean
    
    def getXk(self):
        return self.x_k
    


a = [64.67, 65.46, 190.92, 39.19, 104.44, 28.77]
b = [795.5, 1448.6, 838.1, 696.1, 1150.5, 903.2]
c = [1.15, 0.82, 1.53, 2.46, 0.5, 0.71]
pd = 1150
numIter = 1
limIter = 25
numAgents = 6

Fcentral = FMeanCentral(numAgents, pd, limIter)

def agent(a,b,c,numIter,limIter,id_agente):
    
    P_d = Fcentral.P_d
    numAgents = Fcentral.numAgents
    agente = AgentP2P(a, b, c, P_d, id_agente,numAgents)
    
    fi_0 = agente.getFi()
    x0 = agente.getXk()
    
    fi = fi_0
    xk = x0
    
    Fcentral.refreshLists(fi,xk, id_agente)
    Fcentral.changeIter()
    
    contIter = 0
    
    while contIter < limIter:
        flagContinue = Fcentral.getFlagAgent(id_agente)
        
        if flagContinue:
            print("Iteracion: ", contIter)
            fmean = Fcentral.getFmean()
            agente.setF_mean(fmean)
            agente.calculateXk()
            fi = agente.getFi()
            xk = agente.getXk()
            
            print("agente " + str(id_agente) + ": ",xk)
            
            Fcentral.refreshLists(fi,xk, id_agente)
            
            Fcentral.changeIter()
            
            contIter += 1
            
    Fcentral.saveEvolution(agente.p_evulution, agente.fi_evolution, id_agente)
    

hiloAgente1 = threading.Thread(target=agent, args=(a[0], b[0], c[0], numIter, limIter, 0),name='agente 1')
hiloAgente2 = threading.Thread(target=agent, args=(a[1], b[1], c[1], numIter, limIter, 1),name='agente 2')
hiloAgente3 = threading.Thread(target=agent, args=(a[2], b[2], c[2], numIter, limIter, 2),name='agente 3')
hiloAgente4 = threading.Thread(target=agent, args=(a[3], b[3], c[3], numIter, limIter, 3),name='agente 4')
hiloAgente5 = threading.Thread(target=agent, args=(a[4], b[4], c[4], numIter, limIter, 4),name='agente 5')
hiloAgente6 = threading.Thread(target=agent, args=(a[5], b[5], c[5], numIter, limIter, 5),name='agente 6')

hiloAgente1.start()
hiloAgente2.start()
hiloAgente3.start()
hiloAgente4.start()
hiloAgente5.start()
hiloAgente6.start()
            
            
P = Fcentral.listX_i
P_evol = Fcentral.getListsX_evol()
fi_evol = Fcentral.getListsFi_evolve()


    

        
        
        
    
    
    
    
    