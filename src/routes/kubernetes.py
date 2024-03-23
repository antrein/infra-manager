# src/routes/kubernetes.py
from fastapi import APIRouter, HTTPException
from src.logic.kubernetes import create_ns, get_ns, delete_ns, create_ingress, get_production_deployment

# Initialize your API router
kube_router = APIRouter(tags=["Kubernetes"])

@kube_router.get("/namespace", response_model=list)
async def list_namespaces():
    result = get_ns()
    if result["success"]:
        return result["data"]
    else:
        raise HTTPException(status_code=500, detail=result["message"])
    
@kube_router.post("/project/{project_id}", status_code=200)
async def create_project(project_id: str):
    # Create namespace
    ns_result = create_ns(project_id)
    if not ns_result["success"]:
        raise HTTPException(status_code=400, detail=ns_result["message"])
    
    # Get Production Pods
    deploy_result = get_production_deployment(project_id)

    # Create ingress
    ingress_result = create_ingress(project_id)

    # Rollback
    if not ingress_result["success"]:
        # Attempt to delete namespace if ingress creation fails
        delete_ns(project_id)
        raise HTTPException(status_code=400, detail=ingress_result["message"])
    

    return {"message": f"project {project_id} and associated ingress created successfully"}


@kube_router.delete("/project/{project_id}", status_code=200)
async def delete_project(project_id: str):
    result = delete_ns(project_id)
    if result["success"]:
        return {"message": result["message"]}
    else:
        raise HTTPException(status_code=400, detail=result["message"])
    
