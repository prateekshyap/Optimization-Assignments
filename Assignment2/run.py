from Simplex import Simplex
from fractions import Fraction

class Variable:
	"""docstring for Variable"""
	__sign = False
	__coeff = 0
	__varName = ''
	def __init__(self, s, c, v):
		if (s == '+'):
			self.__sign = True
		elif (s == '-'):
			self.__sign = False
		self.__coeff = c
		self.__varName = v
	def setSign(self,s):
		self.__sign = s
	def setCoeff(self,c):
		self.__coeff = c
	def setVarName(self,v):
		self.__varName = v
	def getSign(self):
		if (self.__sign):
			return '+'
		else:
			return '-'
	def getCoeff(self):
		return self.__coeff
	def getVarName(self):
		return self.__varName
	# def printVar(self):
	# 	if (self.__sign):
	# 		print('+ ',self.__coeff,' ',self.__varName,' ',end='')
	# 	else:
	# 		print('- ',self.__coeff,' ',self.__varName,' ',end='')


z = []
Ai = []
A = [[]]
comp = []
b = []
limits = []
bounds = []
index = 0
coeff = 0.0
i = 0
j = 0
line = ''
target = ''
mode = ''
sign = ''
varName = ''
newVar = Variable(True,0,'')


fileName = input('Enter File Name:')
file = open(fileName,"r")
for line in file:
	tokens = line.split()
	if tokens[0] == 'Maximize' or tokens[0] == 'Minimize' or tokens[0] == 'Subject' or tokens[0] == 'Bounds' or tokens[0] == 'General':
		if tokens[0] == 'Maximize' or tokens[0] == 'Minimize':
			target = tokens[0]
		mode = tokens[0]
		continue
	if mode == 'Maximize' or mode == 'Minimize':
		index = 1
		sign  = '+'
		coeff = 1
		while index < len(tokens):
			if tokens[index] == '-':
				sign = '-'
			elif tokens[index] == '+':
				sign = '+'
			elif tokens[index].isnumeric():
				coeff = int(tokens[index])
			elif tokens[index] != '+':
				varName = tokens[index]
				newVar = Variable(sign,coeff,varName)
				z.append(newVar)
				coeff = 1
			index += 1
	elif mode == 'Subject':
		Ai = []
		index = 1
		sign = '+'
		coeff = 1
		while index < len(tokens):
			if tokens[index] == '-':
				sign = '-'
			elif tokens[index] == '+':
				sign = '+'
			elif tokens[index].isnumeric():
				coeff = int(tokens[index])
			elif tokens[index] == '>' or tokens[index] == '<' or tokens[index] == '>=' or tokens[index] == '<=' or tokens[index] == '=':
				comp.append(tokens[index])
				break
			else:
				varName = tokens[index]
				newVar = Variable(sign,coeff,varName)
				Ai.append(newVar)
				coeff = 1
			index += 1
		A.append(Ai)
		b.append(int(tokens[index+1]))
	elif mode == 'Bounds':
		Ai = []
		newVar = Variable('+',1,tokens[2])
		Ai.append(newVar)
		A.append(Ai)
		if tokens[1] == '<':
			comp.append('>')
		elif tokens[1] == '>':
			comp.append('<')
		elif tokens[1] == '<=':
			comp.append('>=')
		elif tokens[1] == '>=':
			comp.append('<=')
		else:
			comp.append('=')
		b.append(int(tokens[0]))
		Ai = []
		newVar = Variable('+',1,tokens[2])
		Ai.append(newVar)
		A.append(Ai)
		comp.append(tokens[3])
		b.append(int(tokens[4]))

A.pop(0)
# print(target)
# for i in range(len(z)):
# 	z[i].printVar()
# print()
# print('Subject To')
# for i in range(len(A)):
# 	Ai = A[i]
# 	for j in range(len(Ai)):
# 		Ai[j].printVar()
# 	print(' ',comp[i],' ',b[i])


lhsEq = ''
if (z[0].getSign() == '-'):
	lhsEq = '-'
lhsEq += str(z[0].getCoeff())
currVarName = z[0].getVarName()
lhsEq += currVarName[0]
lhsEq += '_'
lhsEq += currVarName[1:len(currVarName)]
lhsEq += ' '

for i in range(1,len(z)):
	lhsEq += z[i].getSign()
	lhsEq += ' '
	lhsEq += str(z[i].getCoeff())
	currVarName = z[i].getVarName()
	lhsEq += (currVarName)[0]
	lhsEq += '_'
	lhsEq += currVarName[1:len(currVarName)]
	lhsEq += ' '
objective = (target.lower(),lhsEq.strip())

constraints = []
for i in range(len(A)):
	Ai = A[i]
	lhsEq = ''
	if (Ai[0].getSign() == '-'):
		lhsEq = '-'
	lhsEq += str(Ai[0].getCoeff())
	currVarName = Ai[0].getVarName()
	lhsEq += currVarName[0]
	lhsEq += '_'
	lhsEq += currVarName[1:len(currVarName)]
	lhsEq += ' '

	for j in range(1,len(Ai)):
		lhsEq += Ai[j].getSign()
		lhsEq += ' '
		lhsEq += str(Ai[j].getCoeff())
		currVarName = Ai[j].getVarName()
		lhsEq += (currVarName)[0]
		lhsEq += '_'
		lhsEq += currVarName[1:len(currVarName)]
		lhsEq += ' '

	lhsEq += comp[i]
	lhsEq += ' '
	lhsEq += str(b[i])
	constraints.append(lhsEq)

lp_system = Simplex(len(z), constraints, objective)
print(lp_system.solution)
# #{'x_2': Fraction(6, 1), 'x_1': Fraction(2, 1)}
print(lp_system.optimize_val)