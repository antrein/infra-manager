from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status, File, UploadFile
from fastapi.responses import JSONResponse
from src.models.dns import GetDnsRecord, AddDnsRecord
from random import choice, randint
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from datetime import datetime, timedelta
import requests
import json
from src.services.sanitizer import sanitize_dns_list
from dotenv import load_dotenv, dotenv_values

dns_router = APIRouter(
    tags=["DNS"]
)

load_dotenv()
config = dotenv_values(".env")

zone_id = config["CLOUDFLARE_ZONE_ID"]
auth_key = config["CLOUDFLARE_KEY"]
auth_email = config["CLOUDFLARE_EMAIL"]

@dns_router.get("/")
async def get_dns_record():
    try:
        url = "https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records"

        header = {
            "Content-Type": "application/json",
            "X-Auth-Email": auth_email,
            "X-Auth-Key": auth_key
        }

        response = requests.request("GET", url, headers=header)

        # Extract JSON content from the response
        json_content = response.json()

        if response.status_code == 200:
            return JSONResponse(status_code=200, content={
                "status_code": 200,
                "status": "success",
                "message": "DNS record successfully added",
                "data": sanitize_dns_list(json_content)
            })
        elif response.status_code == 400:
            return JSONResponse(status_code=400, content={
                "status_code": 400,
                "status": "failed",
                "message": "Bad Request",
                "data": response.json()
            })
        else:
            return JSONResponse(status_code=500, content={
                "status_code": 500,
                "status": "failed",
                "message": "Internal Server Error",
                "data": response.json()
            })

    except ValueError as e:
        return JSONResponse(status_code=401, content={"message": str(e), "data": {}})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})

@dns_router.post("/")
async def add_dns_record(request: AddDnsRecord):
    try:
        url = "https://api.cloudflare.com/client/v4/zones/"+zone_id+"/dns_records"

        header = {
            "Content-Type": "application/json",
            "X-Auth-Email": auth_email,
            "X-Auth-Key": auth_key
        }

        payload = {
            "content": request.content,
            "name": request.name,
            "proxied": False,
            "type": request.type,
            "comment": "",
            "tags": []
        }
        
        response = requests.request("POST", url, json=payload, headers=header)

        if response.status_code == 200:
            return JSONResponse(status_code=200, content={
                "status_code": 200,
                "status": "success",
                "message": "DNS record successfully added",
                "data": response.json()
            })
        elif response.status_code == 400:
            return JSONResponse(status_code=400, content={
                "status_code": 400,
                "status": "failed",
                "message": "Bad Request",
                "data": response.json()
            })
        else:
            return JSONResponse(status_code=500, content={
                "status_code": 500,
                "status": "failed",
                "message": "Internal Server Error",
                "data": response.json()
            })

    except ValueError as e:
        return JSONResponse(status_code=401, content={"message": str(e), "data": {}})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})

@dns_router.patch("/")
async def update_dns_record(record_id: str, request: AddDnsRecord):
    try:
        url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records/" + record_id

        header = {
            "Content-Type": "application/json",
            "X-Auth-Email": auth_email,
            "X-Auth-Key": auth_key
        }

        payload = {
            "content": request.content,
            "name": request.name,
            "proxied": False,
            "type": request.type,
            "comment": "",
            "tags": []
        }
        
        response = requests.request("PATCH", url, json=payload, headers=header)

        if response.status_code == 200:
            return JSONResponse(status_code=200, content={
                "status_code": 200,
                "status": "success",
                "message": "DNS record successfully added",
                "data": response.json()
            })
        elif response.status_code == 400:
            return JSONResponse(status_code=400, content={
                "status_code": 400,
                "status": "failed",
                "message": "Bad Request",
                "data": response.json()
            })
        else:
            return JSONResponse(status_code=500, content={
                "status_code": 500,
                "status": "failed",
                "message": "Internal Server Error",
                "data": {}
            })

    except ValueError as e:
        return JSONResponse(status_code=401, content={"message": str(e), "data": {}})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})

@dns_router.delete("/")
async def delete_dns_record(record_id: str):
    try:
        url = "https://api.cloudflare.com/client/v4/zones/" + zone_id + "/dns_records/" + record_id

        header = {
            "Content-Type": "application/json",
            "X-Auth-Email": auth_email,
            "X-Auth-Key": auth_key
        }

        response = requests.request("DELETE", url, headers=header)

        if response.status_code == 200:
            return JSONResponse(status_code=200, content={
                "status_code": 200,
                "status": "success",
                "message": "DNS record successfully added",
                "data": response.json()
            })
        elif response.status_code == 400:
            return JSONResponse(status_code=400, content={
                "status_code": 400,
                "status": "failed",
                "message": "Bad Request",
                "data": response.json()
            })
        else:
            return JSONResponse(status_code=500, content={
                "status_code": 500,
                "status": "failed",
                "message": "Internal Server Error",
                "data": {}
            })

    except ValueError as e:
        return JSONResponse(status_code=401, content={"message": str(e), "data": {}})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})