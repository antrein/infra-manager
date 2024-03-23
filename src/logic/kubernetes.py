# src/logic/kubernetes.py
from src.services.shell import run_shell, replace_and_run_shell
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

github_pat = config["GITHUB_PAT"]

# NAMESPACE MANAGEMENT
def get_ns():
    script_path = 'script/shell/namespaces/get.sh'
    output = run_shell(script_path)
    if output:
        namespaces = output.strip().split('\n')[1:]  # Skip header
        return {"success": True, "data": namespaces}
    else:
        return {"success": False, "message": "Failed to fetch namespaces"}

def create_ns(project_id):
    script_path = 'script/shell/namespaces/create.sh'
    replacements = {'{{project_id}}': project_id}
    success = replace_and_run_shell(script_path, replacements)
    if success:
        return {"success": True, "message": f"Namespace {project_id} created successfully"}
    else:
        return {"success": False, "message": f"Failed to create namespace for {project_id}"}

def delete_ns(project_id):
    script_path = 'script/shell/namespaces/delete.sh'
    replacements = {'{{project_id}}': project_id}
    success = replace_and_run_shell(script_path, replacements)
    if success:
        return {"success": True, "message": f"Project {project_id} deleted successfully"}
    else:
        return {"success": False, "message": f"Failed to delete namespace {project_id}"}
    
######################################
    
# INGRESS MANAGEMENT

def create_ingress(project_id):
    script_path = 'script/shell/ingress/create.sh'
    replacements = {'{{project_id}}': project_id}
    
    # Run the script after replacements
    result = replace_and_run_shell(script_path, replacements)
    
    # Check the success status of the operation and return a message accordingly
    if isinstance(result, dict) and result.get("success"):
        return {"success": True, "message": f"Ingress for {project_id} created successfully"}
    elif isinstance(result, dict):
        return {"success": False, "message": f"Failed to create Ingress for {project_id}. Error: {result.get('error')}"}
    else:
        return {"success": False, "message": f"An unexpected error occurred when creating Ingress for {project_id}."}
    

######################################
    
# DEPLOYMENT MANAGEMENT
    
def get_production_deployment(project_id):
    script_path = 'script/shell/pods/get-prod.sh'
    replacements = {'{{project_id}}': project_id, '{{github_pat}}': github_pat}
    
    # Run the script after replacements
    result = replace_and_run_shell(script_path, replacements)
    
    # Check the success status of the operation and return a message accordingly
    if isinstance(result, dict) and result.get("success"):
        return {"success": True, "message": f"Ingress for {project_id} created successfully"}
    elif isinstance(result, dict):
        return {"success": False, "message": f"Failed to create Ingress for {project_id}. Error: {result.get('error')}"}
    else:
        return {"success": False, "message": f"An unexpected error occurred when creating Ingress for {project_id}."}
