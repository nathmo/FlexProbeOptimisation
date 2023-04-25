"""
truc a calculer :
1) E(x) [J] : Energie potentielle élastique totale du corps d’épreuve en fonction du déplacement x.
Il s’agit de la somme des énergies potentielles élastiques de toutes les articulations flexibles :
E(x) = E1(x) + E2(x) + ... + En(x).

2)  (x) [N] : Caractéristique force-déformation non-linéaire du corps d’épreuve : F (x) = dE(x)/dx

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

"""
# b largeur, h épaisseur, l longeur
# Energie ressort = 0.5*K*x^2
# K_RCC (N/m)= (l^2+3pl+3p^2)(8*E*b*h^3)/(l^3*12)
# K_Col (Nm/rad)  = (2*E*b*pow(e,2.5))/(9*pi*sqrt(r))
# K_table (N/m) = (2*E*b*h^3)/(l^3)
# K_neg (N/m) =

import math
import matplotlib.pyplot as plt
import numpy as np
class SpringBlade:
  def __init__(self, b, l, h, E):
    self.b = b # blade width (metal block thickness
    self.l = l # blade lenght
    self.h = h # blade thickness (EDM thickness)
    self.E = E # young modulus
  def k(self, x, x1, x2):
      # (l^2)(8*E*b*h^3)/(l^3*24)
      return (pow(self.l, 2))*(8*self.E*self.b*pow(self.h, 3))/(pow(self.l, 3)*24)
  def energyStored(self, x, x1, x2):
      return 0.5*self.k(x, x1, x2)*pow(x, 2)
  def print(self):
      print("I'm a simple blade")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))
      print("K = " + str(self.k()))

class Table2Lame(SpringBlade):
  def k(self, x, x1, x2):
      # (2*E*b*h^3)/(l^3)
      return 2*self.E*self.b*pow((self.h/self.l), 3)
  def print(self):
      print("I'm a 2 Blade Table")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))
      print("K = " + str(self.k()))

class RCCPivot(SpringBlade):
  def __init__(self, b, l, h, E, p):
    super().__init__(b, l, h, E)
    self.p = p # dead zone of the hinge
  def k(self, x, x1, x2):
      # (l^2+3pl+3p^2)(8*E*b*h^3)/(l^3*12)
      return 2*(pow(self.l, 2)+3*self.p*self.l+3*pow(self.p, 2))*(8*self.E*self.b*pow(self.h, 3))/(pow(self.l, 3)*24)
  def print(self):
      print("I'm a RCC Pivot")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))
      print("K = " + str(self.k()))

class NeckedDownColPivot(SpringBlade):
  def __init__(self, b, l, h, E, r, e):
    super().__init__(b, l, h, E)
    self.r = r # blade width (metal block thickness
    self.e = e # blade lenght
  def k(self, x, x1, x2):
      # (2*E*b*pow(e,2.5))/(9*pi*sqrt(r))
      return (2*self.E*self.b*pow(self.e, 2.5))/(9*math.pi*math.sqrt(self.r))
  def print(self):
      print("I'm a necked down Pivot")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))
      print("K = " + str(self.k()))

class NegativeRigidityBlade(SpringBlade):
  def __init__(self, b, l, h, E, p):
    super().__init__(b, l, h, E)
    self.p = p # dead zone of the hinge
  def k(self, x, x1, x2):
      # K=sqrt(F(x)/EI)
      # p = preel / l
      # 2*(EIK)(Kl*cos(Kl)-sin(Kl)[1+(Kl)^2p+(Kl)^2p^2])/(Klsin(Kl)+2(cos(Kl)-1))
      f=x1
      K=math.sqrt(f/(self.b*pow(self.h, 3)*self.E))
      p=self.p / self.l
      return 2*(self.E*self.b*pow(self.h, 3)*K)*(K*self.l*math.cos(K*self.l)-math.sin(K*self.l)*(1+pow(K*self.l, 2)*p/self.l+pow(K*self.p, 2)))/(12*(K*self.l*math.sin(K*self.l)+2*(math.cos(K*self.l)-1)))
  def print(self):
      print("I'm a negative stiffnessRCC pivot down Pivot")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))
      print("K = " + str(self.k()))

def main():
    x = np.linspace(-0.001, 0.001, 100)

    """
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
    # Define the mecanism
    pivotRCC    = RCCPivot(0.01, 0.02, 0.0001, 200000000000, 0.0075)
    table       = Table2Lame(0.01, 0.02, 0.0001, 200000000000)
    col         = NeckedDownColPivot(0.01, 0.02, 0.0001, 200000000000, 0.003, 0.0001)
    negativeRCC = NegativeRigidityBlade(0.01, 0.02, 0.0001, 200000000000, 0.0075)
    # the function, which is y = x^2 here
    x1 = 7623.805
    x2 = 0
    y = pivotRCC.energyStored(x, x1, x2) + table.energyStored(x, x1, x2) + col.energyStored(x, x1, x2) + negativeRCC.energyStored(x, x1, x2)

    # setting the axes at the centre
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('center')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # plot the function
    plt.plot(x, y, 'r')

    # show the plot
    plt.show()

if __name__ == "__main__":
    main()
