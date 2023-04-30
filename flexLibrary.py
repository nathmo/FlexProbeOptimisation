import math
from mpmath import mp

class SpringBlade:
  def __init__(self, b, l, h, E):
    self.b = b # blade width (metal block thickness
    self.l = l # blade lenght
    self.h = h # blade thickness (EDM thickness)
    self.E = E # young modulus
  def k(self, x, x1, x2):
      # I=bh^3/12
      # K=12*E*I/l^3
      I = (self.b * pow(self.h, 3)) / (12)
      return (12*self.E*I)/(pow(self.l, 3))
  def energyStored(self, x, x1, x2):
      return 0.5*self.k(x, x1, x2)*pow(x, 2)
  def show(self):
      print("I'm a simple blade")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))

class NegativeRigidityBlade(SpringBlade):
  def k(self, x, x1, x2):
      """
        $N_0 = \text{charge à appliquer sur la lame pour une rigidité nul}$
        $N = \text{charge à appliquer sur la lame}$
        $E = \text{module de young}$
        $l = \text{longeur de la laimme}$
        $b = \text{largeur de la lame}$
        $h = \text{épaisseur de la lame}$
        $$I = \frac{b*h^3}{12}$$
        $$\gamma = \frac{N}{N_0}$$
        $$N_0=\frac{\pi ^2 *E*I}{l^2}$$
        $$K_0=\frac{12*E*I}{l^3}$$
        $$z(\gamma)=\frac{\gamma*\pi ^2}{12(\frac{2}{\pi*\sqrt{\gamma}}*tan(\frac{\pi*\sqrt{\gamma}}{2})-1)}$$
        $$K=K_0*Z(\gamma)$$
        apres simplification :
        $$I = \frac{b*h^3}{12}$$
        $$Q=\frac{2}{\pi*\sqrt{\frac{N*l^2}{\pi ^2 *E*I}}}$$
        $$K=\frac{N}{l*(Q*tan(\frac{1}{Q})-1)}$$
      :param x:
      :param x1:
      :param x2:
      :return:
      """
      N=x1
      I = (self.b*pow(self.h, 3))/(12)
      Q = 2/(mp.pi*mp.sqrt(N*pow(self.l, 2)/(pow(mp.pi, 2)*self.E*I)))
      K = N/(self.l*(Q*mp.tan(1/Q)-1))
      return K

def show(self):
      print("I'm a Negative Rigidity Blade")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))

class Table2Lame(SpringBlade):
  def k(self, x, x1, x2):
      # I=bh^3/12
      # K=2*12*E*I/l^3  (2 fois car 2 lame)
      I = (self.b * pow(self.h, 3)) / (12)
      return 2*(12*self.E*I)/(pow(self.l, 3))
  def show(self):
      print("I'm a 2 Blade Table")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))

class RCCPivot(SpringBlade):
  def __init__(self, b, l, h, E, p):
    super().__init__(b, l, h, E)
    self.p = p # dead zone of the hinge
  def k(self, x, x1, x2):
      # (l^2+3pl+3p^2)(8*E*b*h^3)/(l^3*12)
      return 2*(pow(self.l, 2)+3*self.p*self.l+3*pow(self.p, 2))*(8*self.E*self.b*pow(self.h, 3))/(pow(self.l, 3)*24)
  def show(self):
      print("I'm a RCC Pivot")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))


class NeckedDownColPivot(SpringBlade):
  def __init__(self, b, l, h, E, r, e):
    super().__init__(b, l, h, E)
    self.r = r # blade width (metal block thickness
    self.e = e # blade lenght
  def k(self, x, x1, x2):
      # (2*E*b*pow(e,2.5))/(9*pi*sqrt(r))
      return (2*self.E*self.b*pow(self.e, 2.5))/(9*math.pi*math.sqrt(self.r))
  def show(self):
      print("I'm a necked down Pivot")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))


class NegativeRigidityRCC(SpringBlade):
  def __init__(self, b, l, h, E, p):
    super().__init__(b, l, h, E)
    self.p = p # dead zone of the hinge
  def k(self, x, x1, x2):
      # K=sqrt(F(x)/EI)
      # p = preel / l
      # 2*(EIK)(Kl*cos(Kl)-sin(Kl)[1+(Kl)^2p+(Kl)^2p^2])/(Klsin(Kl)+2(cos(Kl)-1))
      f=x1 # force of preload from x1
      I= self.b*self.h*self.h*self.h/12
      R = 0.02
      A = math.sqrt(f / (self.E * I))
      B = 4 * self.E * I * (1 + 3 * self.p / self.l + 3 * pow(self.p / self.l, 2)) / (self.l * R * R)
      C = 2 * self.E * I * A * (
                  A * self.l * math.cos(A * self.l) - math.sin(A * self.l) * (1 + pow(A, 2) * self.l * self.p + pow(A * self.p, 2))) / (
                      R * R * (A * self.l * math.sin(A * self.l)) + 2 * (math.cos(A * self.l) - 1))
      return B+C
  def show(self):
      print("I'm a TIVOT beware im untested an might wrong !")
      print("width = "+str(self.b))
      print("lenght = " + str(self.l))
      print("thickness = " + str(self.h))
      print("Young modulus = " + str(self.E))