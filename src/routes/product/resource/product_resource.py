from fastapi import APIRouter,HTTPException

from routes.product.service.product_service import ProductService
from routes.product.domain.models.product_request import ProductRequest
from routes.product.domain.models.product_response import ProductResponse

CONTEXT_PATH = "product"

productRouter = APIRouter(
    prefix=f"/api/v1/{CONTEXT_PATH}",
    tags=[CONTEXT_PATH]
)


@productRouter.post("/symbolic", response_model=ProductResponse, status_code=200)
async def symbolic_product(request : ProductRequest) -> ProductResponse :
    try :
        response = ProductService().symbolicProduct(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    

@productRouter.post("/numeric", response_model=ProductResponse, status_code=200)
async def numeric_product(request : ProductRequest) -> ProductResponse :
    try :
        response = ProductService().numericProduct(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))
    
    