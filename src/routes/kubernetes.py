from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from kubernetes import client, config, watch
from typing import List

# Initialize your API router
kube_router = APIRouter(tags=["Kubernetes"])

# Assuming your Kubernetes cluster configuration is accessible,
# load the kube config. In a cloud environment, this might be different.
config.load_kube_config()

@kube_router.get("/namespaces", response_model=List[str])
async def list_namespaces():
    try:
        # Initialize the Kubernetes client
        v1 = client.CoreV1Api()
        
        # Fetch all namespaces
        namespaces = v1.list_namespace()
        
        # Extract the names of the namespaces
        namespace_names = [namespace.metadata.name for namespace in namespaces.items]
        
        # Return the list of namespace names
        return namespace_names

    except client.ApiException as e:
        # If there's an API exception, return a 500 error
        return JSONResponse(status_code=500, content={"message": "Failed to fetch namespaces", "data": {}})
    except Exception as e:
        # For any other exceptions, return a 500 error
        return JSONResponse(status_code=500, content={"message": str(e), "data": {}})
