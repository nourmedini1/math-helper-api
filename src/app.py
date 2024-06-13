from fastapi import FastAPI 
from routes.complex.resource.complex_resource import complexRouter
from routes.derivatives.resource.derivatives_resource import derivativesRouter
from routes.differential_equations.resource.differential_equations_resource import differentialEquationsRouter

app = FastAPI()

app.include_router(complexRouter)
app.include_router(derivativesRouter)
app.include_router(differentialEquationsRouter)

@app.get("/") 
def read_root():
    return "Hello mathHelper"

