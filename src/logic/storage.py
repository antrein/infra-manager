from google.cloud import storage
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
import io
from fastapi import FastAPI, File, HTTPException, APIRouter, UploadFile
from pydantic import ValidationError
from src.models.storage import UploadFileRequest, FileCategory
from dotenv import load_dotenv, dotenv_values

bucket_name = "antrein-ta"
MAX_FILE_SIZE_MB = 30
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def get_gcs_client():
    key_path = "service-account/gcp.json"
    credentials = service_account.Credentials.from_service_account_file(key_path)
    return storage.Client(credentials=credentials)

def upload_html(file_name, contents):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"html_templates/{file_name}")
    blob.upload_from_string(contents, content_type='text/html')
    url = f"https://storage.googleapis.com/{bucket_name}/html_templates/{file_name}"
    return url

def upload_assets(file_name, contents):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"assets/{file_name}")
    blob.upload_from_file(io.BytesIO(contents))
    url = f"https://storage.googleapis.com/{bucket_name}/assets/{file_name}"
    return url

def delete_file(file_category: str, file_name: str) -> bool:
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    folder = "html_templates" if file_category == "html" else "assets"
    blob = bucket.blob(f"{folder}/{file_name}")
    try:
        blob.delete()
        return True
    except NotFound:
        return False

def list_files(file_category: str):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    folder = "html_templates" if file_category == "html" else "assets"
    blobs = bucket.list_blobs(prefix=folder)
    files = [blob.name for blob in blobs if not blob.name.endswith('/')]
    return files

def create_html_file(file_name: str, html_content: str) -> bytes:
    return html_content.encode('utf-8')