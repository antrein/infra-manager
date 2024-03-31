# src/logic/kubernetes.py
from src.services.shell import run_shell, replace_and_run_shell
from dotenv import load_dotenv, dotenv_values
from src.models.kubernetes import UrlRedirectRequest

load_dotenv()
config = dotenv_values(".env")

github_pat = config["GITHUB_PAT"]
be_mode = config["BE_MODE"]

# NAMESPACE MANAGEMENT
def get_ns():
    try:
        script_path = 'script/shell/namespaces/get.sh'
        output = run_shell(script_path)
        non_project_ns = ["cert-manager", "default", "ingress-nginx", "kube-node-lease", "kube-public", "kube-system", "production", "staging"]
        if output:
            namespaces = output.strip().split('\n')[1:]  # Skip header
            names = [" ".join(item.split()[:-2]).strip() for item in namespaces]
            sanitized_names = [name for name in names if name not in non_project_ns]
            return {"success": True, "data": sanitized_names}
        else:
            return {"success": False, "message": "Failed to fetch namespaces"}
    except Exception as e:
        return {"success": False, "message": f"An exception occurred: {str(e)}"}

def create_ns(project_id):
    try:
        script_path = 'script/shell/namespaces/create.sh'
        replacements = {'{{project_id}}': project_id}
        success = replace_and_run_shell(script_path, replacements)
        if success:
            return {"success": True, "message": f"Namespace {project_id} created successfully"}
        else:
            return {"success": False, "message": f"Failed to create namespace for {project_id}"}
    except Exception as e:
        return {"success": False, "message": f"An exception occurred: {str(e)}"}

def delete_ns(project_id):
    try:
        script_path = 'script/shell/namespaces/delete.sh'
        replacements = {'{{project_id}}': project_id}
        success = replace_and_run_shell(script_path, replacements)
        if success:
            return {"success": True, "message": f"Project {project_id} deleted successfully"}
        else:
            return {"success": False, "message": f"Failed to delete namespace {project_id}"}
    except Exception as e:
        return {"success": False, "message": f"An exception occurred: {str(e)}"}
    
######################################
    
# INGRESS MANAGEMENT

def create_ingress(project_id):
    try:
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
    except Exception as e:
        return {"success": False, "message": f"An exception occurred: {str(e)}"}
    

######################################
    
# DEPLOYMENT MANAGEMENT
    
def get_production_deployment(project_id):
    try:
        script_path = 'script/shell/pods/get-prod.sh'
        replacements = {'{{project_id}}': project_id, '{{github_pat}}': github_pat, '{{be_mode}}': be_mode}
        
        # Run the script after replacements
        result = replace_and_run_shell(script_path, replacements)
        
        # Check the success status of the operation and return a message accordingly
        if isinstance(result, dict) and result.get("success"):
            return {"success": True, "message": f"Workloads {project_id} created successfully"}
        elif isinstance(result, dict):
            return {"success": False, "message": f"Failed to create workloads for {project_id}. Error: {result.get('error')}"}
        else:
            return {"success": False, "message": f"An unexpected error occurred when creating workloads for {project_id}."}
    except Exception as e:
        return {"success": False, "message": f"An exception occurred: {str(e)}"}
    
def rolling_upgrade():
    try: 
        # Get the list of project_id from get_ns()
        project_ids = get_ns()

        if project_ids is None:
            return {"success": False, "message": "Failed to retrieve project IDs."}

        if len(project_ids["data"]) == 0:
            return {"success": True, "message": "No project detected."}

        # If the retrieval is successful
        if project_ids["success"]:
            # Iterate over each project_id
            for project_id in project_ids["data"]:
                # Define replacements for the script

                replacements = {'{{project_id}}': project_id, '{{github_pat}}': github_pat, '{{be_mode}}': be_mode}

                # Define the script path
                script_path = 'script/shell/pods/get-prod.sh'

                # Run the script after replacements
                result = replace_and_run_shell(script_path, replacements)

                # Check the success status of the operation and return a message accordingly
                if result.get("success"):
                    return {"success": True, "message": f"Workloads {project_id} created successfully"}
                else:
                    return {"success": False, "message": f"Failed to create workloads for {project_id}. Error: {result.get('error')}"}
        else:
            # If retrieval fails, return an error message
            return {"success": False, "message": "Failed to retrieve project IDs."}
    except Exception as e:
        return {"success": False, "message": f"An exception occurred: {str(e)}"}
######################################
    
# DEPLOYMENT MANAGEMENT
    
def create_redirect(project_id, project_domain, url_path):
    try:
        script_path = 'script/shell/ingress/redirect.sh'
        replacements = {'{{project_id}}': project_id, '{{project_domain}}': project_domain, '{{url_path}}': url_path}
        
        # Run the script after replacements
        result = replace_and_run_shell(script_path, replacements)
        
        # Check the success status of the operation and return a message accordingly
        if isinstance(result, dict) and result.get("success"):
            return {"success": True, "message": f"Workloads {project_id} created successfully"}
        elif isinstance(result, dict):
            return {"success": False, "message": f"Failed to create workloads for {project_id}. Error: {result.get('error')}"}
        else:
            return {"success": False, "message": f"An unexpected error occurred when creating workloads for {project_id}."}
    except Exception as e:
        return {"success": False, "message": f"An exception occurred: {str(e)}"}