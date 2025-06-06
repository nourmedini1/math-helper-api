from fastapi import FastAPI 
from routes.complex.resource.complex_resource import complexRouter
from routes.derivatives.resource.derivatives_resource import derivativesRouter
from routes.differential_equations.resource.differential_equations_resource import differentialEquationsRouter
from routes.integrals.resource.integrals_resource import integralsRouter
from routes.limits.resource.limits_resource import limitsRouter
from routes.taylor_series.resource.taylor_series_resource import taylorSeriesRouter
from routes.sum.resource.sum_resource import sumRouter
from routes.product.resource.product_resource import productRouter
from routes.linear_systems.resource.linear_systems_resource import linearSystemsRouter
from routes.matrix.resource.matrix_operations_resource import matrixOperationsRouter
from routes.function_plotting.resource.function_plotting_resource import functionPlottingRouter


app = FastAPI()

app.include_router(complexRouter)
app.include_router(derivativesRouter)
app.include_router(differentialEquationsRouter)
app.include_router(integralsRouter)
app.include_router(limitsRouter)
app.include_router(taylorSeriesRouter)
app.include_router(sumRouter)
app.include_router(productRouter)
app.include_router(linearSystemsRouter)
app.include_router(matrixOperationsRouter)
app.include_router(functionPlottingRouter)


@app.get("/") 
def math_helper_root_path():
    return {"value": "welcome to math helper api"}

