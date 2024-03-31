from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, validator

class UrlRedirectRequest(BaseModel):
    project_id: str
    project_domain: str
    url_path: str