from Simplex import Simplex
from fractions import Fraction

class Variable:
	"""docstring for Variable"""
	__sign = False
	__coeff = 0
	__varName = ''
	def __init__(self):
		self.__sign = True
		self.__coeff = 0
		self.__varName = ''
	def __init__(self, s, c, v):
		self.__sign = s
		self.__coeff = c
		self.__varName = v
	def setSign(self,s):
		self.__sign = s
	def setCoeff(self,c):
		self.__coeff = c
	def setVarName(self,v):
		self.__varName = v
	def getSign(self,s):
		return self.__sign
	def getCoeff(self,c):
		return self.__coeff
	def getVarName(self,v):
		return self.__varName
	def printVar(self):
		if (self.__sign):
			print('+ ',self.__coeff,' ',self.__varName,' ')
		else:
			print('- ',self.__coeff,' ',self.__varName,' ')


z = []
Ai = []
A = [[]]
comp = []
b = []
limits = []
bounds = []
index = 0
coeff = 0
j = 0


fileName = input('Enter File Name:')
file = open(fileName,"r")



objective = ('maximize','2x_1 + 5x_2')
constraints = ['1x_1 + 1x_2 <= 6', '1x_2 <= 3', '1x_1 + 2x_2 <= 9']
lp_system = Simplex(2, constraints, objective)
print(lp_system.solution)
#{'x_2': Fraction(6, 1), 'x_1': Fraction(2, 1)}
print(lp_system.optimize_val)