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

forceMin = 0
forceMax = 0
rangeMin = 0
rangeMax = 0

def computeRigidityTableZero(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    x = np.linspace(rangeMin, rangeMax, 100)  # position
    yE = []
    for j in range(0, len(x)):
        Etot = 0
        for part in mechanism:
            Etot = Etot + mp.diff(lambda x: part.energyStored(x, 0, 0), x[j],2)
        yE.append(Etot.real)
    # plot the function
    plt.plot(x, yE, 'r')
    plt.savefig('computeRigidityTableZero.png')
    plt.savefig(os.path.join(path, 'computeRigidityTableZero.png'))

def computeRigidityTableKeq(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    f = np.linspace(forceMin, forceMax, 10)  # force Preload
    x = np.linspace(rangeMin, rangeMax, 100)  # position
    for i in range(0, len(f)):
        yE = []
        for j in range(0, len(x)):
            Etot = 0
            for part in mechanism:
                Etot = Etot + mp.diff(lambda x: part.energyStored(x, f[i], 0), x[j],2)
            yE.append(Etot.real)
        # plot the function
        plt.plot(x, yE, 'r')
    plt.savefig('computeRigidityTableKeq.png')
    plt.savefig(os.path.join(path, 'computeRigidityTableKeq.png'))
def computeEnergy(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    f = np.linspace(forceMin, forceMax, 20)  # force Preload
    x = np.linspace(rangeMin, rangeMax, 100)  # position
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
    plt.savefig('EnergyAsPreloadPosition.png')
    plt.savefig(os.path.join(path, 'EnergyAsPreloadPosition.png'))

def computeEnergyk_minPart(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    f = 5.67  # force Preload (force such that minimum k_eq)
    x = np.linspace(rangeMin, rangeMax, 100)  # position
    for part in mechanism:
        y = []
        for j in range(0, len(x)):
            y.append(part.energyStored(x[j], f, 0).real)
        # plot the function
        plt.plot(x, y, 'b')
    # save the plot
    plt.savefig('computeEnergyk_minPart.png')
    plt.savefig(os.path.join(path, 'computeEnergyk_minPart.png'))

def computeForceAsPositionANDPreload(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    f = np.linspace(forceMin, forceMax, 20)  # force Preload
    x = np.linspace(rangeMin, rangeMax, 100)  # position
    for i in range(0, len(f)):
        yE = []
        for j in range(0, len(x)):
            Etot = 0
            for part in mechanism:
                Etot = Etot + mp.diff(lambda x: part.energyStored(x, f[i], 0), x[j])
            yE.append(Etot.real)
        # plot the function
        plt.plot(x, yE, 'r')
    plt.savefig('ForceAsPositionANDPreload.png')
    plt.savefig(os.path.join(path, 'ForceAsPositionANDPreload.png'))

def computeForceAsPositionANDPreloadTaylor(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    f = np.linspace(forceMin, forceMax, 20)  # force Preload
    x = np.linspace(rangeMin, rangeMax, 100)  # position
    for i in range(0, len(f)):
        yE = []
        for j in range(0, len(x)):
            Etot = 0
            for part in mechanism:
                Etot = Etot + mp.diff(lambda x: part.energyStored(x, f[i], 0), x[j])
            yE.append(Etot.real)
        # plot the function
        plt.plot(x, yE, 'g')
    plt.savefig('ForceAsPositionANDPreloadPolynomial.png')
    plt.savefig(os.path.join(path, 'ForceAsPositionANDPreloadPolynomial.png'))

def computeRigidityAsPositionANDPreload(mechanism, path):
    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    f = np.linspace(forceMin, forceMax, 10)  # force Preload
    x = np.linspace(rangeMin, rangeMax, 100)  # position
    for i in range(0, len(f)):
        yE = []
        for j in range(0, len(x)):
            Etot = 0
            for part in mechanism:
                Etot = Etot + mp.diff(lambda x: part.energyStored(x, f[i], 0), x[j],2)
            yE.append(Etot.real)
        # plot the function
        plt.plot(x, yE, 'r')
    plt.savefig('RigidityAsPositionANDPreload.png')
    plt.savefig(os.path.join(path, 'RigidityAsPositionANDPreload.png'))

def computeMu(mechanism, newpath):
    # Read in the file
    filedata = ""
    dataout = ""
    with open('report.md') as f:
        for line in (f):
            filedata = filedata + line.replace('mu_r', 'mu_r = '+str(3))
    # Write the file out again
    with open('report.md', 'wt') as file:
        file.write(filedata)

def main():
    # set the precision
    mp.dps = 20 #number of significant digit used for calculation
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
        result = 0
        if(str(row[2]) == "mm"):
            result = ureg.parse_expression((str(row[1])+" "+str(row[2]))).to(ureg.meter) #convert it to meter
        else:
            result = ureg.parse_expression((str(row[1])+" "+str(row[2])))
        parameters[row[0]] = result.magnitude
    print(parameters)

    global forceMin   # deso pas deso
    global forceMax
    global rangeMin
    global rangeMax
    forceMin = parameters["forceMinRigidity"]
    forceMax = parameters["forceMaxRigidity"]
    rangeMin = parameters["rangeXProbeMin"]  # -0.0006 #-0.0011
    rangeMax = parameters["rangeXProbeMax"]  # 0.0006 #0.0011
    # define the mechanism
    print("--------------------------------------------")
    b_wheel = parameters["thicknessWheelPlate"] # 8 mm
    b_converter = parameters["thicknessConverterPlate"]  # 8 mm
    E = parameters["Eyoung"]  #200 GPa steel, 110 titanium
    pivotRCC      = RCCPivot(b_wheel , parameters["BladeLengthRCC"], parameters["BladeThicknessRCC"], E, f_XtoRotation, parameters["RCCdeadCenter"]) # +- 1'000. N/m after conversion from Couple/rad
    wheelAnchor   = SpringBlade(b_converter, parameters["bladeLengthWheelAnchor"], parameters["bladeThicknessWheelAnchor"], E, f_XYRotation) #
    negativeBladePusher = NegativeRigidityBlade(b_converter, parameters["bladeLengthTablePushing"], parameters["bladeThicknessTablePushing"], E, f_x) #250 N/m
    negativeBlade = NegativeRigidityBlade(b_converter, parameters["bladeLengthTable"], parameters["bladeThicknessTable"], E, f_x)  # 250 N/m
    ForceConverter = SpringBlade(b_converter, parameters["bladeLengthForceConverter"], parameters["bladeThicknessForceConverter"], E, f_x)  # 250 N/m
    ZeroConverter = SpringBlade(b_wheel, parameters["bladeLengthZeroConverter"], parameters["bladeThicknessZeroConverter"], E, f_Xby8)  # 2000 N/m
    mechanismZero = [ZeroConverter, ZeroConverter]  # reglage zero
    mechanismKeqForce = [ForceConverter, ForceConverter] # k_eq
    mechanism = [pivotRCC, pivotRCC, wheelAnchor, wheelAnchor, negativeBladePusher, negativeBladePusher, negativeBladePusher, negativeBlade, negativeBlade , negativeBlade, ZeroConverter, ZeroConverter]
    print("mechanism definition :")
    for part in mechanism:
        print("")
        part.show()

    # create a new folder and copy xlsx parameter to the folder
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
    print("created new folder with result :" + newpath)
    print("---------------------------------------------------------")
    # generate the graphs and save them to a new folder + update the one here

    # 1) rigidité de la table de réglage du zéro en fonction du moteur de réglage du zéro.
    print("compute Zéro offset table Rigidity")
    computeRigidityTableZero(mechanismZero, newpath)
    # 2) rigidité de la table de réglage du k_eq en fonction du moteur de réglage du k_eq.
    print("compute Keq table Rigidity and offset")
    computeRigidityTableKeq(mechanismKeqForce, newpath)
    # 6) E(x) [J] : Energie potentielle élastique totale du corps d’épreuve en fonction du déplacement x.
    print("compute Energy")
    computeEnergy(mechanism, newpath)
    computeEnergyk_minPart(mechanism, newpath)
    # 7)  (x) [N] : Caractéristique force-déformation non-linéaire du corps d’épreuve : F (x) = dE(x)/dx
    print("compute Force as deformation")
    computeForceAsPositionANDPreload(mechanism, newpath)
    # 8) Polynome qui approxime 2)
    print("compute Force as deformation Polynomial")
    computeForceAsPositionANDPreloadTaylor(mechanism, newpath)
    # 9) rigidité en fonction de la position et de la précontrainte
    print("compute Rigidity")
    computeRigidityAsPositionANDPreload(mechanism, newpath)
    # 10) compute non linéarity
    print("compute non linearity")
    computeMu(mechanism, newpath)

    # Final, saving result in template
    print("saving result to report")
    shutil.copyfile("report.md", os.path.join(newpath, "report.md"))
if __name__ == "__main__":
    main()
    print("done")
