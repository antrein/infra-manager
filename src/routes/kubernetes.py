# src/routes/kubernetes.py
from fastapi import APIRouter, HTTPException
from src.logic.kubernetes import create_ns, get_ns, delete_ns, create_ingress, get_production_deployment, rolling_upgrade, create_redirect
from src.models.kubernetes import UrlRedirectRequest

# Initialize your API router
kube_router = APIRouter(tags=["Kubernetes"])

@kube_router.get("/rolling-ugrade", response_model=dict)
async def rolling_upgrade_project():
    result = rolling_upgrade()
    print(result)
    if result["success"]:
        return {"message": "Success upgrade to the latest version."}
    else:
        raise HTTPException(status_code=500, detail=result["message"])

@kube_router.get("/project", response_model=dict)
async def list_project():
    result = get_ns()
    if result["success"]:
        return {"data": result["data"]}
    else:
        raise HTTPException(status_code=500, detail=result["message"])
    
@kube_router.post("/project/", status_code=200)
async def create_project(request: UrlRedirectRequest):
    # Create namespace
    ns_result = create_ns(request.project_id)
    if not ns_result["success"]:
        raise HTTPException(status_code=400, detail=ns_result["message"])
    
    # Get Production Pods
    deploy_result = get_production_deployment(request.project_id)

    # Create ingress
    ingress_result = create_ingress(request.project_id)

    # Create Redirect
    redirect_result = create_redirect(request.project_id, request.project_domain, request.url_path)

    # Rollback
    if not ingress_result["success"]:
        # Attempt to delete namespace if ingress creation fails
        delete_ns(request.project_id)
        raise HTTPException(status_code=400, detail=ingress_result["message"])
    

    return {"message": f"project {request.project_id} created successfully"}


@kube_router.delete("/project/{project_id}", status_code=200)
async def delete_project(project_id: str):
    result = delete_ns(project_id)
    if result["success"]:
        return {"message": f"project {project_id} deleted successfully"}
    else:
        raise HTTPException(status_code=400, detail=result["message"])
    
