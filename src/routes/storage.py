from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import ValidationError
from src.logic.storage import upload_to_bucket, create_html_file, delete_file
from src.models.storage import UploadFileRequest
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

infra_mode = config["INFRA_MODE"]

storage_router = APIRouter(tags=["Storage"])

@storage_router.post("/upload/")
async def upload_file(upload_file_request: UploadFileRequest):
    try:
        # Decode the base64 HTML content
        html_content = upload_file_request.get_decoded_html_content()

        # Create HTML file content as bytes
        contents = create_html_file(upload_file_request.file_name, html_content)
        
        # Upload to bucket and get the URL
        url = upload_to_bucket(f"{upload_file_request.file_name}.html", contents)
        
        return {
            "status": "success",
            "message": "File uploaded successfully",
            "data": {
                "url": url
            }
        }
    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@storage_router.delete("/file/{file_name}")
async def delete_file_endpoint(file_name: str):
    try:
        success = delete_file(file_name)
        if not success:
            raise HTTPException(status_code=404, detail="File not found")
        
        return {
            "status": "success",
            "message": "File deleted successfully"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))