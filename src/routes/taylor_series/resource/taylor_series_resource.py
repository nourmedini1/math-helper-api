from fastapi import APIRouter,HTTPException
from routes.taylor_series.service.taylor_series_service import TaylorSeriesService
from routes.taylor_series.domain.models.taylor_series_request import TaylorSeriesRequest
from routes.taylor_series.domain.models.taylor_series_response import TaylorSeriesResponse


CONTEXT_PATH = "taylor-series"
taylorSeriesRouter = APIRouter(prefix=f"/api/v1/{CONTEXT_PATH}", tags=["taylor series"])

@taylorSeriesRouter.post("/expand", response_model=TaylorSeriesResponse, status_code=200)
async def taylor_series(request : TaylorSeriesRequest) -> TaylorSeriesResponse :
    try :
        response = TaylorSeriesService().taylorSeries(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=400,detail= str(e))