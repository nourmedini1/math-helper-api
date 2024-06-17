from typing import List

class MatrixUtils :
    @staticmethod
    def createIdentityMatrix(matrixOrder : int) -> List[List[float]]:
        identity = []
        for i in range(matrixOrder) :
            row = []
            for j in range(matrixOrder) :
                if i == j :
                    row.append(1)
                else :
                    row.append(0)
            identity.append(row)
        return identity
    
    @staticmethod
    def createElementaryMatrix(matrixOrder : int,effectedRow : int,effectedColumn : int,value : float) -> List[List[float]]:
        elementaryMatrix = MatrixUtils.createIdentityMatrix(matrixOrder)
        elementaryMatrix[effectedRow][effectedColumn] = value
        return elementaryMatrix
    
    @staticmethod
    def fetchRowToChange(matrix : List[List[float]],row : List[float]) -> int:
        for i in range(len(matrix)) :
            if matrix[i] == row :
                return i
            
    @staticmethod
    def createNullVector(matrixOrder : int) -> List[float]:
        return [0 for _ in range(matrixOrder)]
    
    @staticmethod
    def checkRowDuplication(matrix : List[List[float]]) -> bool:
        for i in range(len(matrix)) :
            for j in range(i+1,len(matrix)) :
                if matrix[i] == matrix[j] :
                    return True
        else :
            return False 

    @staticmethod  
    def checkNullColumn(matrix : List[List[float]]) -> bool:
        nullVector = MatrixUtils.createNullVector(len(matrix))
        for i in range(len(matrix)):
                column = []
                for j in range(len(matrix)):
                    column.append(matrix[j][i])
                if column == nullVector:
                    return True
        else:
            return False
        
    @staticmethod
    def checkNullRow(matrix : List[List[float]]) -> bool:
        nullVector = MatrixUtils.createNullVector(len(matrix))
        for i in range(len(matrix)):
                row = []
                for j in range(len(matrix)):
                    row.append(matrix[i][j])
                if row == nullVector:
                    return True
        else:
            return False
        
    @staticmethod
    def checkInversibility(matrix : List[List[float]]) -> bool:
        hasNullColumn = MatrixUtils.checkNullColumn(matrix)
        hasNullRow = MatrixUtils.checkNullRow(matrix)
        hasDuplicateRows = MatrixUtils.checkRowDuplication(matrix)
        if hasDuplicateRows or hasNullColumn or hasNullRow :
            return False
        else :
            return True
        
    @staticmethod
    def permuteWhenNull(matrix : List[List[float]],nullValueRow : int,nullValueColumn : int) -> List[List[float]]:
        stop = False
        i = nullValueRow
        while i < len(matrix) - 1 and not stop:
            j = i + 1
            while j in range(i + 1, len(matrix)) and not stop:
                if matrix[j][nullValueColumn] != 0:
                    permute_tmp = []
                    permute_tmp = matrix[i]
                    matrix[i] = matrix[j]
                    matrix[j] = permute_tmp
                    stop = True
                j += 1
            i += 1
        return matrix
    
    @staticmethod
    def permuteForOperation(matrix  : List[List[float]],row1 : int,row2 : int) :
        tmp = matrix[row1]
        matrix[row1] = matrix[row2]
        matrix[row2] = tmp
        return matrix
    
    @staticmethod
    def multiplyMatrixes(matrixA : List[List[float]], matrixB : List[List[float]]) -> List[List[float]]:
        resultMatrix = []
        n = len(matrixA)
        for i in range(n):
            row = []
            for j in range(n):
                row.append(0)
            resultMatrix.append(row)

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    resultMatrix[i][j] += matrixA[i][k] * matrixB[k][j]
        return resultMatrix
    

    @staticmethod
    def neautralizePivot(matrix : List[List[float]],identity : List[List[float]],matrixOrder : int,i : int,j : int) -> tuple[List[List[float]]]:
        pivotForOperation = matrix[i][j]
        elementaryMatrix = MatrixUtils.createElementaryMatrix(matrixOrder,i,j,1/pivotForOperation)
        matrix = MatrixUtils.multiplyMatrixes(elementaryMatrix,matrix)
        identity = MatrixUtils.multiplyMatrixes(elementaryMatrix,identity)
        return matrix,identity
    
    @staticmethod
    def applyOperationOnMatrix(matrix : List[List[float]],identity : List[List[float]],matrixOrder : int,i : int,j : int) -> tuple[List[List[float]]]:
        for k in range(matrixOrder) :
            if k != i and matrix[k][j] != 0 :
                elementaryMatrix = MatrixUtils.createElementaryMatrix(matrixOrder,k,j,-matrix[k][j])
                matrix = MatrixUtils.multiplyMatrixes(elementaryMatrix,matrix)
                identity = MatrixUtils.multiplyMatrixes(elementaryMatrix,identity)
        return matrix,identity

    

    

        
    
