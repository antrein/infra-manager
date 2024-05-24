from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, validator
import re

class RestartCategory(str, Enum):
    project = "project"
    all = "all"

class UrlRedirectRequest(BaseModel):
    project_id: str
    project_domain: str = Field(...)
    url_path: str = Field(default="/")

    @validator('project_domain')
    def validate_domain(cls, v):
        if '://' in v:
            raise ValueError('Domain must not include protocol (http or https)')
        if v.startswith('/') or v.endswith('/'):
            raise ValueError('Domain must not start or end with a slash')

        # Enhanced regular expression for validating a domain name with at least one dot
        # if not re.match(r'^[a-zA-Z\d-]{1,63}(\.[a-zA-Z\d-]{1,63})+$', v):
        #     raise ValueError('Invalid domain format')

        return v

    @validator('url_path')
    def validate_path(cls, v):
        if len(v) == 1:
            if v != '/':
                raise ValueError('Url path of one character must be "/"')
        else:
            if not v.startswith('/'):
                raise ValueError('Url path must start with a "/"')
            if not v.endswith('/'):
                raise ValueError('Url path must end with a "/"')
        return v

    @validator('project_id')
    def validate_project_id(cls, v):
        if not v.isalnum():
            raise ValueError('Project ID must be alphanumeric')
        if not v.lower() == v:
            raise ValueError('Project ID must be in lowercase')
        return v
    
class RestartRequest(BaseModel):
    category: RestartCategory