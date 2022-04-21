from fractions import Fraction
from warnings import warn

class Simplex(object):
    def __init__(self, noOfVariables, constraints, objectiveFunction):
        """
        noOfVariables: Number of variables
        equations: A list of strings representing constraints
        """
        self.noOfVariables = noOfVariables
        self.constraints = constraints
        self.objective = objectiveFunction[0]
        self.objectiveFunction = objectiveFunction[1]
        self.coeffMatrix, self.rRows, self.noOfSVariables, self.noOfRVariables = self.constructMatrixFromConstraints()
        del self.constraints
        self.basicVariables = [0 for i in range(len(self.coeffMatrix))] # set basic variables as zero
        self.phase1() # call phase 1
        rIndex = self.noOfRVariables + self.noOfSVariables

        for i in self.basicVariables: # for each basic variable
            if i > rIndex: # if it is greater than rIndex
                raise ValueError("Infeasible Solution") # solution is infeasible

        self.deleteRVariables() # delete the additional variables

        if 'min' in self.objective.lower(): # if the objective is to minimize
            self.solution = self.objectiveMinimize() # call minimize function

        else: # otherwise
            self.solution = self.objectiveMaximize() # call maximize function
        self.optVal = self.coeffMatrix[0][-1] # store the optimal value

    def constructMatrixFromConstraints(self):
        noOfSVariables = 0  # number of slack and surplus variables
        noOfRVariables = 0  # number of additional variables to balance equality and less than equal to
        for expression in self.constraints: # for each constraint
            if '>=' in expression: # if greater than equal to
                noOfSVariables += 1 # increase slack variables

            elif '<=' in expression: # if less than equal to
                noOfSVariables += 1 # increase slack variables
                noOfRVariables += 1 # increase additional variables

            elif '=' in expression: # if equal to
                noOfRVariables += 1 # increase additional variables
        totalVariables = self.noOfVariables + noOfSVariables + noOfRVariables # total number of variables

        coeffMatrix = [[Fraction("0/1") for i in range(totalVariables+1)] for j in range(len(self.constraints)+1)]
        sIndex = self.noOfVariables
        rIndex = self.noOfVariables + noOfSVariables
        rRows = [] # stores the non zero index of r
        for i in range(1, len(self.constraints)+1):
            constraint = self.constraints[i-1].split(' ') # split constraints by space

            for j in range(len(constraint)): # for each constraint

                if '_' in constraint[j]: # if there is an underscore
                    coeff, index = constraint[j].split('_') # get the coefficient and index
                    if constraint[j-1] is '-': # if sign is negative
                        coeffMatrix[i][int(index)-1] = Fraction("-" + coeff[:-1] + "/1")
                    else:
                        coeffMatrix[i][int(index)-1] = Fraction(coeff[:-1] + "/1")

                elif constraint[j] == '<=': # if less than equal to
                    coeffMatrix[i][sIndex] = Fraction("1/1")  # add surplus variable
                    sIndex += 1

                elif constraint[j] == '>=': # if greater than equal to
                    coeffMatrix[i][sIndex] = Fraction("-1/1")  # slack variable
                    coeffMatrix[i][rIndex] = Fraction("1/1")   # r variable
                    sIndex += 1
                    rIndex += 1
                    rRows.append(i)

                elif constraint[j] == '=': # if equal to
                    coeffMatrix[i][rIndex] = Fraction("1/1")  # r variable
                    rIndex += 1
                    rRows.append(i)

            coeffMatrix[i][-1] = Fraction(constraint[-1] + "/1")

        return coeffMatrix, rRows, noOfSVariables, noOfRVariables

    def phase1(self):
        rIndex = self.noOfVariables + self.noOfSVariables # add number of surplus variables
        for i in range(rIndex, len(self.coeffMatrix[0])-1): # for each coefficient
            self.coeffMatrix[0][i] = Fraction("-1/1") # set fraction
        coeff0 = 0
        for i in self.rRows: # for each non zero row
            self.coeffMatrix[0] = addRow(self.coeffMatrix[0], self.coeffMatrix[i]) # add the row
            self.basicVariables[i] = rIndex # store the basic variables
            rIndex += 1
        sIndex = self.noOfVariables
        for i in range(1, len(self.basicVariables)): # for each basic variable
            if self.basicVariables[i] == 0: # if it is 0
                self.basicVariables[i] = sIndex # store sindex
                sIndex += 1

        # run simplex iterations
        keyColumn = maxIndex(self.coeffMatrix[0]) # get the mazimum index
        condition = self.coeffMatrix[0][keyColumn] > 0

        while condition is True:

            keyRow = self.findKeyRow(keyColumn = keyColumn)
            self.basicVariables[keyRow] = keyColumn
            pivot = self.coeffMatrix[keyRow][keyColumn]
            self.normalizeToPivot(keyRow, pivot)
            self.makeKeyColumnZero(keyColumn, keyRow)

            keyColumn = maxIndex(self.coeffMatrix[0])
            condition = self.coeffMatrix[0][keyColumn] > 0

    def findKeyRow(self, keyColumn):
        minVal = float("inf")
        minI = 0
        for i in range(1, len(self.coeffMatrix)): # for each coefficient
            if self.coeffMatrix[i][keyColumn] > 0: # if greater than zero
                val = self.coeffMatrix[i][-1] / self.coeffMatrix[i][keyColumn] # divide the maximum column
                if val <  minVal: # update the minimum value
                    minVal = val
                    minI = i
        if minVal == float("inf"): # if minimum value is not updated
            raise ValueError("Unbounded Solution") # Solution is unbounded
        if minVal == 0: # if minimum value is 0
            warn("Dengeneracy") # Degeneracy condition
        return minI

    def normalizeToPivot(self, keyRow, pivot):
        for i in range(len(self.coeffMatrix[0])): # for each coefficient
            self.coeffMatrix[keyRow][i] /= pivot # divide the pivot

    def makeKeyColumnZero(self, keyColumn, keyRow):
        num_columns = len(self.coeffMatrix[0])
        for i in range(len(self.coeffMatrix)): # for each coefficient
            if i != keyRow:
                factor = self.coeffMatrix[i][keyColumn] # get the factor
                for j in range(num_columns): # for each column
                    self.coeffMatrix[i][j] -= self.coeffMatrix[keyRow][j] * factor # multiply the factor

    def deleteRVariables(self):
        for i in range(len(self.coeffMatrix)): # for each coefficient
            nonRLength = self.noOfVariables + self.noOfSVariables + 1 # add the number of variables and surplus variables
            length = len(self.coeffMatrix[i]) # get the length
            while length != nonRLength: # till the length gets equal
                del self.coeffMatrix[i][nonRLength-1] # delete the coefficient
                length -= 1 # reduce the length by 1

    def updateObjectiveFunction(self):
        objectiveFunctionCoeffs = self.objectiveFunction.split()
        for i in range(len(objectiveFunctionCoeffs)): # for each variable in objective function
            if '_' in objectiveFunctionCoeffs[i]: # if there is an underscore
                coeff, index = objectiveFunctionCoeffs[i].split('_') # split from underscore
                if objectiveFunctionCoeffs[i-1] is '-': # if sign is negative
                    self.coeffMatrix[0][int(index)-1] = Fraction(coeff[:-1] + "/1")
                else:
                    self.coeffMatrix[0][int(index)-1] = Fraction("-" + coeff[:-1] + "/1")

    def checkAlternateSolution(self):
        for i in range(len(self.coeffMatrix[0])):
            if self.coeffMatrix[0][i] and i not in self.basicVariables[1:]:
                # warn("Alternative Solution Exists")
                break

    def objectiveMinimize(self):
        self.updateObjectiveFunction()

        for row, column in enumerate(self.basicVariables[1:]): # for each basic variable
            if self.coeffMatrix[0][column] != 0: # if non zero coefficient
                self.coeffMatrix[0] = addRow(self.coeffMatrix[0], multiplyConstRow(-self.coeffMatrix[0][column], self.coeffMatrix[row+1])) # add row

        # run simplex iterations
        keyColumn = maxIndex(self.coeffMatrix[0]) # get the maximum index
        condition = self.coeffMatrix[0][keyColumn] > 0

        while condition is True:

            keyRow = self.findKeyRow(keyColumn = keyColumn)
            self.basicVariables[keyRow] = keyColumn
            pivot = self.coeffMatrix[keyRow][keyColumn]
            self.normalizeToPivot(keyRow, pivot)
            self.makeKeyColumnZero(keyColumn, keyRow)

            keyColumn = maxIndex(self.coeffMatrix[0])
            condition = self.coeffMatrix[0][keyColumn] > 0

        solution = {}
        for i, var in enumerate(self.basicVariables[1:]):
            if var < self.noOfVariables:
                solution['x_'+str(var+1)] = self.coeffMatrix[i+1][-1]

        for i in range(0, self.noOfVariables):
            if i not in self.basicVariables[1:]:
                solution['x_'+str(i+1)] = Fraction("0/1")
        self.checkAlternateSolution()
        return solution

    def objectiveMaximize(self):
        self.updateObjectiveFunction()

        for row, column in enumerate(self.basicVariables[1:]): # for each basic variable
            if self.coeffMatrix[0][column] != 0: # if non zero coefficient
                self.coeffMatrix[0] = addRow(self.coeffMatrix[0], multiplyConstRow(-self.coeffMatrix[0][column], self.coeffMatrix[row+1]))

        # run simplex iterations
        keyColumn = minIndex(self.coeffMatrix[0]) # get the maximum index
        condition = self.coeffMatrix[0][keyColumn] < 0

        while condition is True:

            keyRow = self.findKeyRow(keyColumn = keyColumn)
            self.basicVariables[keyRow] = keyColumn
            pivot = self.coeffMatrix[keyRow][keyColumn]
            self.normalizeToPivot(keyRow, pivot)
            self.makeKeyColumnZero(keyColumn, keyRow)

            keyColumn = minIndex(self.coeffMatrix[0])
            condition = self.coeffMatrix[0][keyColumn] < 0

        solution = {}
        for i, var in enumerate(self.basicVariables[1:]):
            if var < self.noOfVariables:
                solution['x_'+str(var+1)] = self.coeffMatrix[i+1][-1]

        for i in range(0, self.noOfVariables):
            if i not in self.basicVariables[1:]:
                solution['x_'+str(i+1)] = Fraction("0/1")

        self.checkAlternateSolution()

        return solution

def addRow(row1, row2):
    row_sum = [0 for i in range(len(row1))]
    for i in range(len(row1)):
        row_sum[i] = row1[i] + row2[i]
    return row_sum

def maxIndex(row):
    max_i = 0
    for i in range(0, len(row)-1):
        if row[i] > row[max_i]:
            max_i = i

    return max_i

def multiplyConstRow(const, row):
    mul_row = []
    for i in row:
        mul_row.append(const*i)
    return mul_row

def minIndex(row):
    minI = 0
    for i in range(0, len(row)):
        if row[minI] > row[i]:
            minI = i

    return minI

