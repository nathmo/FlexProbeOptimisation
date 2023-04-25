from math import*
class Block:
    def __init__(self, thickness, material, name):
        if (type(thickness) == type(material) == float or type(thickness) == type(material) == int) and type(name) == str:
            self.b = thickness
            self.E = material
            self.name = name
        else:
            print("The material" + name + "has not a good configuration, thus none of the data is included")
            print("Please check again your code.")
    def print(self):
        print("The material '"+self.name+"' has been set up with the following properties :")
        print("    Thickness = "+ str(self.b) + " mm")
        print("    Young Modulus = " + str(self.E) + " GPa")

class Blade:
    def __init__(self, main_block, height, length, f_app = 0., name = ""):
        if type(main_block) == Block and (type(height) == type(length) == float or type(height) == type(length) == int):
            self.compound = main_block
            self.name = name
            self.h = height
            self.l = length
            self.f = f_app
        else:
            print("The blade" + name + "has not a good configuration, thus none of the data is included")
            print("Please check again your code.")

    def print(self):
        print("The blade '" + self.name + "' has been set up with the following properties :")
        print("    Compound : b = " + str(self.compound.b) + " mm  E = "+ str(self.compound.E) + "GPa")
        print("    Height = " + str(self.h) + " mm")
        print("    Length = " + str(self.l) + " mm")
        print("    Force Applied = " + str(self.f))

    def k_comp(self):
        return (self.compound.b*self.h*self.compound.E)/(self.l)

    def k_tors(self):
        return (self.compound.E*self.compound.b*(self.h**3))/(4*(self.l**3))

class BladeTable:
    def __int__(self, base, comp = 0., name = ""):
        if type(base) == Blade and (type(comp) == float or type(comp) == int):
            self.blades = base
            self.compression = comp
            self.name = name
        else:
            print("The blade table" + self.name + "has not a good configuration, thus none of the data is included")
            print("Please check again your code.")
    def k_ncomp(self):
        return 2*self.blades.compound.E*self.blades.compound.b*((self.blades.h/self.blades.l)**3)

class RCC_Pivot_45:
    def __init__(self, base):