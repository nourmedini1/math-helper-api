from fastapi import APIRouter, HTTPException
from routes.function_plotting.service.function_plotting_service import FunctionPlottingService
from routes.function_plotting.domain.models.plot_request import PlotRequest
from routes.function_plotting.domain.models.plot_response import PlotResponse


CONTEXT_PATH = "function-plotting"
functionPlottingRouter = APIRouter(
    prefix=f"/api/v1/{CONTEXT_PATH}",
    tags=["Function Plotting"]
)

service = FunctionPlottingService()

@functionPlottingRouter.post("/plot", response_model=PlotResponse, status_code=200)
async def plot_function(request: PlotRequest) -> PlotResponse:
    try:
        response = service.generate_plot_data(
            function=request.function,
            lower_bound=request.lower_bound,
            upper_bound=request.upper_bound,
            precision=request.precision,
            max_points=request.max_points
        )
        return PlotResponse(**response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))