from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
from src.services.refresh_token import refresh_kubectl_token
from src.routes.kubernetes import kube_router
from src.routes.storage import storage_router
from src.middleware.middleware import RefreshTokenMiddleware

from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

app = FastAPI()

# app.add_middleware(RefreshTokenMiddleware)

app.include_router(kube_router, prefix="/kube")
app.include_router(storage_router, prefix="/storage")

@app.get("/")
async def home():
    return {"message": "Antrein Infrastructure Manager", "infra_mode": config["INFRA_MODE"], "be_mode": config["BE_MODE"]}

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000,
                log_level="info")