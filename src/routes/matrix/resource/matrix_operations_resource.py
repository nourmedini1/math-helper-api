import traceback
from fastapi import APIRouter,HTTPException
from routes.matrix.service.matrix_operations_service import MatrixOperationsService
from routes.matrix.domain.models.matrix_request import MatrixRequest
from routes.matrix.domain.models.matrix_response import MatrixResponse

CONTEXT_PATH = "matrix-operations"

matrixOperationsRouter = APIRouter(
    prefix=f"/api/v1/{CONTEXT_PATH}",
    tags=["Matrix Operations"]
)

matrixOperationsService = MatrixOperationsService()

@matrixOperationsRouter.post("/add",status_code=200, response_model=MatrixResponse)
async def add_matrixes(request : MatrixRequest) -> MatrixResponse :
    try :
        response = matrixOperationsService.addMatrixes(request)
        return response
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail= str(e))


@matrixOperationsRouter.post("/multiply",status_code=200, response_model=MatrixResponse)
async def multiply_matrixes(request : MatrixRequest) -> MatrixResponse :
    try :
        response = matrixOperationsService.multiplyMatrixes(request)
        return response
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail= str(e))
     
@matrixOperationsRouter.post("/invert",status_code=200, response_model=MatrixResponse)
async def invert_matrix(request : MatrixRequest) -> MatrixResponse :
    try :
        response = matrixOperationsService.invertMatrix(request)
        return response
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail= str(e))
    
@matrixOperationsRouter.post("/rank",status_code=200, response_model=MatrixResponse)
async def calculate_matrix_rank(request : MatrixRequest) -> MatrixResponse :
    try :
        response = matrixOperationsService.calculateRank(request)
        return response
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail= str(e))
    
@matrixOperationsRouter.post("/determinant",status_code=200, response_model=MatrixResponse)
async def calculate_determinant(request : MatrixRequest) -> MatrixResponse :
    try :
        response = matrixOperationsService.calculateDeterminant(request)
        return response
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail= str(e))
    
@matrixOperationsRouter.post("/eigen",status_code=200, response_model=MatrixResponse)
async def calculate_eigen_value_and_eigen_vector(request : MatrixRequest) -> MatrixResponse :
    try :
        response = matrixOperationsService.calculateEigen(request)
        return response
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400,detail= str(e))

