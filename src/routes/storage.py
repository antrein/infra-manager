from fastapi import FastAPI, File, HTTPException, APIRouter, UploadFile
from pydantic import ValidationError
from src.logic.storage import list_files, upload_assets, upload_html, create_html_file, delete_file
from src.models.storage import UploadFileRequest, FileCategory
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

MAX_FILE_SIZE_MB = 30
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

infra_mode = config["INFRA_MODE"]

storage_router = APIRouter(tags=["Storage"])

@storage_router.post("/html")
async def upload_html_file(upload_file_request: UploadFileRequest):
    try:
        html_content = upload_file_request.get_decoded_html_content()
        contents = create_html_file(upload_file_request.file_name, html_content)
        url = upload_html(f"{upload_file_request.file_name}.html", contents)
        return {"status": "success", "message": "File uploaded successfully", "data": {"url": url}}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@storage_router.post("/assets")
async def upload_asset(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        file_size = len(contents)
        if file_size > MAX_FILE_SIZE_BYTES:
            raise HTTPException(status_code=413, detail=f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB}MB")
        
        file_name = file.filename
        url = upload_assets(file_name, contents)
        return {"status": "success", "message": "File uploaded successfully", "data": {"url": url}}
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@storage_router.delete("/file")
async def delete_file_endpoint(file_category: FileCategory, file_name: str):
    try:
        success = delete_file(file_category.value, file_name)
        if not success:
            raise HTTPException(status_code=404, detail="File not found")
        return {"status": "success", "message": "File deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@storage_router.get("/list")
async def list_file_endpoint(file_category: FileCategory):
    try:
        files = list_files(file_category.value)
        return {"status": "success", "message": "Files listed successfully", "data": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
