from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router.login.route import router as login

from router.lotes.lotes import router as lotes
from router.mensajero.mensajero import router as mensajero

app = FastAPI(
    title="Mi API",
    version="1.0.0",
    description="API de ejemplo con rutas modulares"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye TODOS los endpoints definidos en la carpeta /rutas
app.include_router(login)
app.include_router(lotes)
app.include_router(mensajero)

@app.get("/", tags=["Root"])
def root():
    return {"message": "API funcionando. Ve a /docs para probar el login."}