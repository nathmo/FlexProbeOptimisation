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
from mouvmentConversionLibrary import *
import openpyxl
import logging
from pint import UnitRegistry
import shutil

def computeEnergy(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    f = np.linspace(-0.00001, -0.1, 100)  # force Preload
    x = np.linspace(-0.0005, 0.0005, 100)  # position
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
    plt.savefig(os.path.join(path, 'EnergyAsPreloadPosition.png'))

def computeRigidity(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    yK = []

    f = np.linspace(0.00001, 0.1, 100)  # force Preload
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
    b_wheel = 0.008 # 8 mm
    b_converter = 0.004  # 8 mm
    E = 200000000000 #200 GPa
    pivotRCC      = RCCPivot(b_wheel , 0.018, parameters["BladeThicknessRCC"], E, f_XtoRotation, 0.005) # +- 1'000. N/m after conversion from Couple/rad
    wheelAnchor   = SpringBlade(b_converter, 0.0075, parameters["bladeThicknessWheelAnchor"], E, f_XYRotation) #
    negativeBladePusher = NegativeRigidityBlade(b_converter, 0.02, parameters["bladeThicknessTablePushing"], E, f_x) #250 N/m
    negativeBlade = NegativeRigidityBlade(b_converter, 0.02, parameters["bladeThicknessTable"], E, f_x)  # 250 N/m
    ForceConverter = SpringBlade(b_converter, 0.02, parameters["bladeThicknessForceConverter"], E, f_x)  # 250 N/m
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




if __name__ == "__main__":
    main()
    print("done")
