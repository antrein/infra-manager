from fastapi import APIRouter, HTTPException
from src.logic.kubernetes import (
    create_ns, delete_redirect, get_ns, delete_ns, 
    create_ingress, get_production_deployment, restart_kube, rolling_upgrade, 
    create_redirect, health_check, spin_up
)
from src.services.refresh_token import refresh_kubectl_token
from src.models.kubernetes import RestartCategory, UrlRedirectRequest, RestartRequest
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

infra_mode = config["INFRA_MODE"]

# Initialize your API router
kube_router = APIRouter(tags=["Kubernetes"])

@kube_router.get("/rolling-upgrade", response_model=dict)
async def rolling_upgrade_project():
    result = rolling_upgrade()
    if result["success"]:
        return {"status": "success", "message": "Success upgrade to the latest version.", "data": {}}
    else:
        raise HTTPException(status_code=500, detail={"status": "error", "message": result["message"], "data": {}})

@kube_router.get("/project", response_model=dict)
async def list_project():
    result = get_ns()
    if result["success"]:
        return {"status": "success", "message": "Projects listed successfully.", "data": result["data"]}
    else:
        raise HTTPException(status_code=500, detail={"status": "error", "message": result["message"], "data": {}})
    
@kube_router.post("/project", status_code=200)
async def create_project(request: UrlRedirectRequest):
    # Create namespace
    if infra_mode == "multi":
        ns_result = create_ns(request.project_id)
        if not ns_result["success"]:
            raise HTTPException(status_code=400, detail={"status": "error", "message": ns_result["message"], "data": {}})
    
    if infra_mode == "multi":
        deploy_result = get_production_deployment(request.project_id)
        ingress_result = create_ingress(request.project_id)
    
    redirect_result = create_redirect(request.project_id, request.project_domain, request.url_path, infra_mode)

    # Rollback
    if not redirect_result["success"]:
        # Attempt to delete namespace if ingress creation fails
        delete_ns(request.project_id)
        raise HTTPException(status_code=400, detail={"status": "error", "message": "Failed to create redirect.", "data": {}})
    
    return {"status": "success", "message": f"Project {request.project_id} created successfully", "data": {}}

@kube_router.delete("/restart/{category}", status_code=200)
async def restart(category: RestartCategory):
    result = restart_kube(category)
    if result["success"]:
        return {"status": "success", "message": "All projects have been processed successfully", "data": result.get("results", [])}
    else:
        return {"status": "failure", "message": result.get("message", "Unknown error occurred"), "data": {}}

@kube_router.delete("/project/{project_id}", status_code=200)
async def delete_project(project_id: str):
    result = delete_ns(project_id)
    if result["success"]:
        return {"status": "success", "message": f"Project {project_id} deleted successfully", "data": {}}
    else:
        raise HTTPException(status_code=400, detail={"status": "error", "message": result["message"], "data": {}})

@kube_router.delete("/project/redirect/{project_id}", status_code=200)
async def delete_redirect_router(project_id: str):
    result = delete_redirect(project_id)
    if result["success"]:
        return {"status": "success", "message": f"Redirect for project {project_id} deleted successfully", "data": {}}
    else:
        raise HTTPException(status_code=400, detail={"status": "error", "message": result["message"], "data": {}})
    
@kube_router.get("/health/", response_model=dict)
async def check_health():
    result = health_check_all()
    if not result['success']:
        # If health_check fails to execute properly, provide a detailed error message
        raise HTTPException(status_code=500, detail={"status": "error", "message": result["message"], "data": {}})

    # Evaluate the total number of deployments
    if result["total_deployments"] == 0:
        # No deployments found in the namespace
        return {
            "status": "failed",
            "message": "No deployments found in the namespace.",
            "data": {}
        }
    else:
        # Check if there are non-ready deployments
        if result["non_ready_deployments"]:
            # There are some deployments not ready
            return {
                "status": "success",
                "message": "Some deployments are not ready.",
                "data": {
                    "healthiness": False,
                    "deployment_names": result["non_ready_deployments"]
                }
            }
        else:
            # All deployments are ready
            return {
                "status": "success",
                "message": "All deployments are healthy.",
                "data": {
                    "healthiness": True
                }
            }

@kube_router.get("/health/{project_id}", response_model=dict)
async def check_health(project_id: str):
    result = health_check(project_id)
    if not result['success']:
        # If health_check fails to execute properly, provide a detailed error message
        raise HTTPException(status_code=500, detail={"status": "error", "message": result["message"], "data": {}})

    # Evaluate the total number of deployments
    if result["total_deployments"] == 0:
        # No deployments found in the namespace
        return {
            "status": "failed",
            "message": "No deployments found in the namespace.",
            "data": {}
        }
    else:
        # Check if there are non-ready deployments
        if result["non_ready_deployments"]:
            # There are some deployments not ready
            return {
                "status": "success",
                "message": "Some deployments are not ready.",
                "data": {
                    "healthiness": False,
                    "deployment_names": result["non_ready_deployments"]
                }
            }
        else:
            # All deployments are ready
            return {
                "status": "success",
                "message": "All deployments are healthy.",
                "data": {
                    "healthiness": True
                }
            }


@kube_router.post("/spin-up", response_model=dict)
async def spin_up_project():
    result = spin_up()
    if result["success"]:
        return {"status": "success", "message": "Spin-up process completed successfully", "data": result["data"]}
    else:
        raise HTTPException(status_code=500, detail={"status": "error", "message": result["message"], "data": {}})