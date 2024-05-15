from pydantic import BaseModel, Field, validator
import re
from bs4 import BeautifulSoup
import base64

class UploadFileRequest(BaseModel):
    file_name: str = Field(..., description="Alphanumeric with no spaces")
    html_base64: str

    @validator('file_name')
    def validate_file_name(cls, v):
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError('file_name must be alphanumeric with no spaces')
        return v

    @validator('html_base64')
    def validate_html_base64(cls, v):
        try:
            decoded_html = base64.b64decode(v).decode('utf-8')
            soup = BeautifulSoup(decoded_html, "html.parser")
            if not soup.find():
                raise ValueError('Invalid HTML content')
        except Exception as e:
            raise ValueError('Invalid HTML content')
        return v

    def get_decoded_html_content(self):
        return base64.b64decode(self.html_base64).decode('utf-8')
