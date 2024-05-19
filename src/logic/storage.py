from google.cloud import storage
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound
import io

bucket_name = "antrein-ta"

def upload_html(file_name, contents):
    key_path = "./service-account/gcp.json"
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"html_templates/{file_name}")
    blob.upload_from_string(contents, content_type='text/html')
    url = f"https://storage.googleapis.com/{bucket_name}/html_templates/{file_name}"
    return url

def upload_assets(file_name, contents):
    key_path = "./service-account/gcp.json"
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = storage.Client(credentials=credentials)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"assets/{file_name}")
    blob.upload_from_file(io.BytesIO(contents))
    url = f"https://storage.googleapis.com/{bucket_name}/assets/{file_name}"
    return url

def delete_file(file_category: str, file_name: str) -> bool:
    # Path to your service account key file
    key_path = "./service-account/gcp.json"
    
    # Authenticate the client with your service account
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = storage.Client(credentials=credentials)
    
    # Get the bucket
    bucket = client.bucket(bucket_name)

    if file_category == "html":
        folder = "html_templates"
    else:
        folder = "assets"
    
    # Create a new blob with the specified folder path
    blob = bucket.blob(f"{folder}/{file_name}")
    
    # Delete the file
    try:
        blob.delete()
        return True
    except NotFound:
        return False

def create_html_file(file_name: str, html_content: str) -> bytes:
    # Create HTML content as bytes
    html_bytes = html_content.encode('utf-8')
    return html_bytes
