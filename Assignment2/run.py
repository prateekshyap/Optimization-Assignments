from Simplex import Simplex
from fractions import Fraction
import time

startTime = time.time()
class Variable: # contains the structure of a variable
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

# declarations
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

# read from input file
fileName = input('Enter File Name:')
file = open(fileName,"r")
for line in file:
	tokens = line.split()
	if tokens[0] == 'Maximize' or tokens[0] == 'Minimize' or tokens[0] == 'Subject' or tokens[0] == 'Bounds' or tokens[0] == 'General': # if the line is not a data
		if tokens[0] == 'Maximize' or tokens[0] == 'Minimize':
			target = tokens[0] # set target
		mode = tokens[0] # set mode
		continue # continue
	if mode == 'Maximize' or mode == 'Minimize': # if mode is to maximize or minimize
		index = 1
		sign  = '+'
		coeff = 1
		while index < len(tokens): # for each token
			if tokens[index] == '-': # set sign
				sign = '-'
			elif tokens[index] == '+': # set sign
				sign = '+'
			elif tokens[index].isnumeric(): # set coefficient
				coeff = int(tokens[index])
			else: # store in z (objective function)
				varName = tokens[index]
				newVar = Variable(sign,coeff,varName)
				z.append(newVar)
				coeff = 1
			index += 1
	elif mode == 'Subject': # if mode is subject to
		Ai = []
		index = 1
		sign = '+'
		coeff = 1
		while index < len(tokens): # for each token
			if tokens[index] == '-': # set sign
				sign = '-'
			elif tokens[index] == '+': # set sign
				sign = '+'
			elif tokens[index].isnumeric(): # set coefficient
				coeff = int(tokens[index])
			elif tokens[index] == '>' or tokens[index] == '<' or tokens[index] == '>=' or tokens[index] == '<=' or tokens[index] == '=': # set comparator
				comp.append(tokens[index])
				break
			else: # append to Ai
				varName = tokens[index]
				newVar = Variable(sign,coeff,varName)
				Ai.append(newVar)
				coeff = 1
			index += 1
		A.append(Ai) # append Ai to A
		b.append(int(tokens[index+1])) # append b
	elif mode == 'Bounds': # if mode is bounds, add both side to A and b
		Ai = []
		newVar = Variable('+',1,tokens[2])
		Ai.append(newVar)
		A.append(Ai)
		# set comparator
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

A.pop(0) # remove the first blank list

# get the objective function
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

# set objective function
objective = (target.lower(),lhsEq.strip())

#get the constraints
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

	# set constraints
	constraints.append(lhsEq)

# set the lp system
lpSystem = Simplex(len(z), constraints, objective)

# print the solution
print('--------------------------------------')
print('               Solution')
print('--------------------------------------')
# print(lpSystem.solution)
for key in lpSystem.solution:
	print(key, '=', lpSystem.solution[key])

# print the objective function
print('--------------------------------------')
print('       Objective Function Value')
print('--------------------------------------')
print('z =',lpSystem.optVal)

# print("%s seconds",(time.time()-startTime))