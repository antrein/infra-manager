from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import schedule
import time
import threading
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

def job():
    print("Running cron refresh_kubectl_token")
    result = refresh_kubectl_token()
    print(f"Result: {result}")

def schedule_jobs():
    schedule.every(1).hour.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # COMMENT THIS WHEN RUNNING IN LOCAL
    refresh_kubectl_token()

    # Run the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=schedule_jobs)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Run FastAPI app
    uvicorn.run('main:app', host='0.0.0.0', port=8000, log_level="info")
