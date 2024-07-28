from routes.matrix.domain.utils.matrix_utils import MatrixUtils
import sympy as smp
import numpy as np
from typing import List
from routes.matrix.domain.models.matrix_request import MatrixRequest
from routes.matrix.domain.models.matrix_response import MatrixResponse



class MatrixOperationsServiceMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MatrixOperationsServiceMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
class MatrixOperationsService(metaclass= MatrixOperationsServiceMeta) :

    def initializeResultMatrix(self, rows : int , colomns : int ) -> List[List[float]] :
        return [[0 for _ in range(colomns)] for _ in range(rows)]

    def addMatrixes(self, request : MatrixRequest) -> MatrixResponse : 
        columns = len(request.matrixA)
        rows = len(request.matrixA[0])
        resultMatrix = self.initializeResultMatrix(rows,columns)
        for i in range(rows):
            for j in range(columns):
                resultMatrix[i][j] = request.matrixA[i][j] + request.matrixB[i][j]
        latexifiedMatrix = smp.latex(smp.Matrix(resultMatrix))
        return MatrixResponse(
            matrix= latexifiedMatrix
        )
    

    def multiplyMatrixes(self, request : MatrixRequest) -> MatrixResponse :
        columnsA = len(request.matrixA)
        columnsB = len(request.matrixB)
        rowsA = len(request.matrixA[0])
        resultMatrix = self.initializeResultMatrix(rowsA,columnsB)
        for i in range(rowsA):
            for j in range(columnsB):
                for k in range(columnsA):
                    resultMatrix[i][j] += request.matrixA[i][k] * request.matrixB[k][j]
        latexifiedMatrix = smp.latex(smp.Matrix(resultMatrix))
        return MatrixResponse(
            matrix=latexifiedMatrix
        )
    
    def invertMatrix(self, request : MatrixRequest) -> MatrixResponse : 
        matrix = request.matrixA
        if MatrixUtils.checkInversibility(request.matrixA) is False :
            raise Exception("Matrix is not invertible")
        else :
            order = len(matrix)
            identity = MatrixUtils.createIdentityMatrix(order)
            for i in range(order) :
                for j in range(order) :
                    if i == j :
                        isPivotZero = matrix[i][j] == 0
                        isPivotOne = matrix[i][j] == 1 
                        if isPivotZero :
                            matrix = MatrixUtils.permuteWhenNull(matrix,i,j)
                            isPivotStillZero = matrix[i][j] == 0 
                            if isPivotStillZero :
                                raise Exception("Matrix is not invertible")
                            identity = MatrixUtils.permuteForOperation(identity,i,MatrixUtils.fetchRowToChange(matrix,matrix[i]))
                        elif isPivotOne is False:
                            matrix,identity = MatrixUtils.neautralizePivot(matrix,identity,order,i,j) 
                        matrix,identity = MatrixUtils.applyOperationOnMatrix(matrix,identity,order,i,j)                    
            resultMatrix = smp.latex(smp.Matrix(identity))
            return MatrixResponse(
                matrix=resultMatrix
            )
        
    def calculateRank(self, request : MatrixRequest) -> MatrixResponse :
        matrix = request.matrixA
        columns = len(request.matrixA)
        rows = len(request.matrixA[0])
        if rows == 1 :
            return MatrixResponse(rank="1")
        for i in range(rows-1) :
            for j in range(columns) :
                if i == j :
                    isPivotZero = matrix[i][j] == 0
                    if isPivotZero :
                        matrix = MatrixUtils.permuteWhenNull(matrix,i,j)
                        isPivotStillZero = matrix[i][j] == 0 
                        if isPivotStillZero :
                            return rows - 1
                        for k in range(i+1,rows) :
                            if matrix[k][j] != 0 :
                                elementaryMatrix = MatrixUtils.createElementaryMatrix(rows,k,j,-(matrix[k][j] / matrix[i][j]))
                                matrix = MatrixUtils.multiplyMatrixes(elementaryMatrix,matrix)
        allZeroRowsCount = 0
        zeros = MatrixUtils.createNullVector(columns)
        for i in range(rows) :
            if matrix[i] == zeros :
                allZeroRowsCount += 1
        return MatrixResponse(rank=min([rows,columns]) - allZeroRowsCount)
    
    def _setupEigenValue(self,eigenValueArray : np.ndarray ) -> str:
        eigenValue = []
        for element in eigenValueArray:
            eigenValue.append(element)
        latexEigenValue = smp.latex(smp.Matrix(eigenValue))
        return latexEigenValue

    def _setupEigenVector(self,eigenVectorArray : np.ndarray) -> str:
        eigenVector = []
        for row in eigenVectorArray:
            l = []
            for element in row:
                l.append(element)
            eigenVector.append(l)
        latexEigenVector = smp.latex(smp.Matrix(eigenVector))
        return latexEigenVector
        
    def calculateEigen(self, request : MatrixRequest) -> MatrixResponse :
        matrixArray = np.array(request.matrixA)
        eigenValueArray, eigenVectorArray = np.linalg.eig(matrixArray)
        return MatrixResponse(
            eigenValue= self._setupEigenValue(eigenValueArray),
            eigenVector = self._setupEigenVector(eigenVectorArray)
        )
    
    def calculateDeterminant(self, request : MatrixRequest) -> MatrixResponse : 
        order = len(request.matrixA)
        matrix = request.matrixA
        if order == 1 :
            return MatrixResponse(determinant=matrix[0][0])
        if order == 2 : 
            return MatrixResponse(determinant= matrix[0][0]*matrix[1][1] + matrix[0][1]*matrix[1][0])
        permutations = []
        for i in range(order-1) :
            for j in range(order) :
                if i == j : 
                    isPivotZero = matrix[i][j] == 0
                    if isPivotZero :
                        matrix = MatrixUtils.permuteWhenNull(matrix,i,j)
                        permutations.append(-1)
                        isPivotStillZero = matrix[i][j] == 0 
                        if isPivotStillZero :
                            return MatrixResponse(determinant="0")
                    for k in range(i+1,order) :
                        if matrix[k][j] != 0 :
                            elementaryMatrix = MatrixUtils.createElementaryMatrix(order,k,j,-(matrix[k][j] / matrix[i][j]))
                            matrix = MatrixUtils.multiplyMatrixes(elementaryMatrix,matrix)
        diagonalProduct = 1 
        for i in range(order) :
            for j in range(order) :
                if i == j :
                    diagonalProduct *= matrix[i][j]  
        for i in range(len(permutations)) :
            diagonalProduct *= permutations[i]
        return MatrixResponse(determinant=str(diagonalProduct))






