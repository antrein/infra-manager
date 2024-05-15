from google.cloud import storage
from google.oauth2 import service_account
from google.api_core.exceptions import NotFound

bucket_name = "antrein-ta"
folder = "html_templates"

def upload_to_bucket(file_name, contents):
    # Path to your service account key file
    key_path = "./service-account/gcp.json"
    
    # Authenticate the client with your service account
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = storage.Client(credentials=credentials)
    
    # Get the bucket
    bucket = client.bucket(bucket_name)
    
    # Create a new blob with the specified folder path and upload the file's content to Google Cloud Storage
    blob = bucket.blob(f"{folder}/{file_name}")
    blob.upload_from_string(contents, content_type='text/html')
    
    # Construct the URL of the uploaded file
    url = f"https://storage.googleapis.com/{bucket_name}/{folder}/{file_name}"
    
    return url

def delete_file(file_name: str) -> bool:
    # Path to your service account key file
    key_path = "./service-account/gcp.json"
    
    # Authenticate the client with your service account
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = storage.Client(credentials=credentials)
    
    # Get the bucket
    bucket = client.bucket(bucket_name)
    
    # Create a new blob with the specified folder path
    blob = bucket.blob(f"{folder}/{file_name}.html")
    
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
