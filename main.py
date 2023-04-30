"""
Ce script calcul les différent parametre d'un système à lame.
Plus spécifiquement, une série de primitive sont définis tel que des lames, des cols, des lames préchargé etc...
il suffit d'utiliser la feuille excel qui est lier au CAD pour changer les parametres.
toutes les figures sont graphé dans des images qui peuvent être visualiser dans un document markdown.

feel free to use this script if its of any help to you.
(no waranty on the exactitude of the result given tho)

TODO : export other settings like force range, mechanism config, etc to a log file
"""

import math
import matplotlib.pyplot as plt
import numpy as np
from mpmath import mp
import pandas as pd
import os
from flexLibrary import *
import openpyxl
import logging
from pint import UnitRegistry
import shutil

def computeEnergy(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    f = np.linspace(-1, 40, 10)  # force Preload
    x = np.linspace(-0.001, 0.001, 100)  # position
    for i in range(0, len(f)):
        yE = []
        for j in range(0, len(x)):
            Etot = 0
            for part in mechanism:
                Etot = Etot + part.energyStored(x[j], f[i], 0)
            yE.append(Etot.real)
        # plot the function
        plt.plot(x, yE, 'b')
    # save the plot
    plt.savefig(os.path.join(path, 'EnergyyAsPreloadPosition.png'))

def computeRigidity(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    yK = []

    f = np.linspace(-1, 40, 10)  # force Preload
    for i in range(0, len(f)):
        ktot = 0
        for part in mechanism:
            ktot = ktot + part.k(0, f[i], 0)
        yK.append(ktot.real)
    # plot the function
    plt.plot(f, yK, 'r')
    plt.savefig(os.path.join(path, 'RigidityAsPreload.png'))

def main():
    # set the precision
    mp.dps = 100 #number of significant digit used for calculation
    print(mp)

    # parse the excel sheet containing the physical parameters (in the Autodesk Inventor Format) (no column title
    # first column = name, seconde column = value, third = unit
    #example : bladeThicknessTablePushing       0.1     mm
    excelPATH = ""
    for file in os.listdir("."):
        if file.endswith(".xlsx"):
            excelPATH = file # only use the first sheet found.
            break
    df = pd.read_excel(excelPATH, header=None)
    print("")
    print("found file : " + str(excelPATH))
    print("here is a sample of what's in it. ensure it looks right.")
    print(df.head())
    print("")
    parameters = {}
    ureg = UnitRegistry()
    for i in range(0, len(df. index)):
        row = df.loc[i, :].values.flatten().tolist() # extract each row as a list
        result = ureg.parse_expression((str(row[1])+" "+str(row[2]))).to(ureg.meter) #convert it to meter
        parameters[row[0]] = result.magnitude
    print(parameters)

    # define the mechanism
    print("--------------------------------------------")
    b = 0.01 # 10 mm
    E = 200000000000 #200 GPa
    h = 0.0001 # 100 micron
    pivotRCC      = RCCPivot(b , 0.018, parameters["BladeThicknessRCC"], E, 0.005) # +- 1'068. N/m after conversion from Couple/rad
    wheelAnchor   = SpringBlade(b, 0.0075, parameters["bladeThicknessWheelAnchor"], E)
    negativeBladePusher = NegativeRigidityBlade(b, 0.02, parameters["bladeThicknessTablePushing"], E) #250 N/m
    negativeBlade = NegativeRigidityBlade(b, 0.02, parameters["bladeThicknessTable"], E)  # 250 N/m
    ForceConverter = SpringBlade(b, 0.02, parameters["bladeThicknessForceConverter"], E)  # 250 N/m
    mechanism = [pivotRCC, pivotRCC,
                 wheelAnchor, wheelAnchor,
                 negativeBladePusher, negativeBladePusher, negativeBladePusher,
                 negativeBlade, negativeBlade , negativeBlade]
    print("mechanism definition :")
    for part in mechanism:
        print("")
        part.show()

    # create a new folder and copy the markdown template + xlsx parameter to the folder
    print("-------------------------------------------------")
    onlydir = [f for f in os.listdir(".") if os.path.isdir(os.path.join(".", f))]
    max = 0
    for folder in onlydir:
        try:
            if int(folder.split("-")[-1]) > max:
                max = int(folder.split("-")[-1])
        except:
            pass
    max = max + 1
    newpath = os.path.join(".", "resultSimulation-"+str(max))
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        shutil.copyfile(excelPATH, os.path.join(newpath, excelPATH))
        shutil.copyfile("report.md", os.path.join(newpath, "report.md"))
    print("create new folder with result :" + newpath)
    # generate the graphs and save them to a new folder
    print("---------------------------------------------------------")
    # 1) E(x) [J] : Energie potentielle élastique totale du corps d’épreuve en fonction du déplacement x.
    print("compute Energy")
    computeEnergy(mechanism, newpath)
    # 2)  (x) [N] : Caractéristique force-déformation non-linéaire du corps d’épreuve : F (x) = dE(x)/dx
    print("compute Rigidity")
    computeRigidity(mechanism, newpath)
    """
    truc a calculer :

Il s’agit de la somme des énergies potentielles élastiques de toutes les articulations flexibles :
E(x) = E1(x) + E2(x) + ... + En(x).



3) Fpoly3(x) [N] : Caractéristique force-déformation approximée par un polynôme de degrés trois :
F (x) ∼= Fpoly3(x) = a0 + a1 · x + a2 · x2 + a3 · x3 ;

4) μ_r : Non-linéarité relative : μr = a3/a1

5) k [N/m] : Rigidité à l’entrée du capteur de force : k = a1 ∼= F/x

6) F_lin(x) [N] : Caractéristique force-déformation linéarisée : F (x) ∼= Flin(x) = k · x

7) s(x) [m] : Déplacement de la cible du capteur de position induit par le déplacement x

8) keq [N/m] : Rigidité équivalente du corps d’épreuve : keq ∼= F/s = k · x/s = k · i. Remarque : une
fois keq connue, la force appliquée est déterminée via la relation F ∼= keq · s

9) S [m/N] : Sensibilité du capteur de force : S = 1/keq

10) RF [N] : Résolution du capteur de force : RF = keq · Rs = k1 · i · Rs

11) Fmax [N] : Etendue de la plage de mesure du capteur de force : Fmax 50mN
avec Fmax ∼= keq · smax

12) DF : Gamme dynamique du capteur de force : DF = Fmax/RF

Avec les valeurs extrêmes du réglage de précharge pmin et pmax nous définissions respectivement :

keq,max et keq,min : bornes de la plage de réglage de rigidité ;

fmin et fmax : fréquences propres du corps d’épreuve

Fmax(keq,max) : plus grande force que peut mesurer le capteur avec son réglage le plus rigide ;

RF(keq,min) : résolution du capteur de force avec son réglage le moins rigide

DFv : gamme dynamique virtuelle du capteur de force : DFv = Fmax(keq,max)/RF(keq,min)

Target :
Plage de mesure : Fmax > 50 mN

Résolution de mesure : RF < 500 nN. Il s’agit du principal critère d’optimisation du capteur
qui consiste à minimiser la valeur RF(keq,min)

Correction du zéro : le système de réglage doit permettre de corriger des forces parasites
selon l’axe X dans l’intervalle suivant : −1 mN <= Fparasite <= 1 mN

2 pivot RCC angulaire
1 table à lame
2 pivot à col
1 lame rigidité négative

    1 pivot RCC angulaire
    1 table à lame
    2 pivot à col
    1 pivot RCC rigidité négative
    
    b, l, h, E, r, e
    
    b blade width (metal block thickness
    l blade lenght
    h blade thickness (EDM thickness)
    E young modulus
    r necked down radius
    e thined zone of necked down
    """




if __name__ == "__main__":
    main()
    print("done")
