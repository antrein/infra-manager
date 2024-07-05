# src/logic/kubernetes.py
from src.services.repos import get_repos_be, get_repos_fe, get_repos_infra
from src.services.shell import run_script, run_shell, replace_and_run_shell
from dotenv import load_dotenv, dotenv_values

load_dotenv()
config = dotenv_values(".env")

github_pat = config["GITHUB_PAT"]
be_mode = config["BE_MODE"]
infra_mode = config["INFRA_MODE"]

# NAMESPACE MANAGEMENT
def get_ns():
    try:
        if infra_mode == "shared": 
            script_path = 'script/shell/namespaces/get-shared.sh'
        else:
            script_path = 'script/shell/namespaces/get.sh'
        output = run_shell(script_path)
        non_project_ns = ["cert-manager", "default", "ingress-nginx", "kube-node-lease", "kube-public", "kube-system", "production", "staging", "utils"]

        if infra_mode == "shared":
            if output:
                namespaces = output.strip().split('\n')[1:]  # Skip header
                return {"success": True, "data": namespaces}
            else:
                return {"success": False, "message": "Failed to fetch namespaces"}
        else:
            if output:
                namespaces = output.strip().split('\n')[1:]  # Skip header
                names = [" ".join(item.split()[:-2]).strip() for item in namespaces]
                if len(names) == 0:
                    return {"success": False, "message": "No namespaces found"}
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
        if infra_mode == "shared": 
            script_path = 'script/shell/namespaces/delete-shared.sh'
        else:
            script_path = 'script/shell/namespaces/delete.sh'

        replacements = {'{{project_id}}': project_id}
        success = replace_and_run_shell(script_path, replacements)
        if success:
            return {"success": True, "message": f"Project {project_id} deleted successfully"}
        else:
            return {"success": False, "message": f"Failed to delete namespace {project_id}"}
    except Exception as e:
        return {"success": False, "message": f"An exception occurred: {str(e)}"}
    
def restart_kube(category):
    try:
        if category == "all":
            deployments = run_script("kubectl get deployments -n production -o jsonpath='{.items[*].metadata.name}'")
            if not deployments["success"]:
                return {"success": False, "message": f"Failed to get deployments: {deployments['error']}"}

            infra_repo = get_repos_infra()

            deployments_list = deployments["output"].strip().split()
            for deployment in deployments_list:
                if deployment not in infra_repo:
                    delete_deployment = run_script(f"kubectl delete deployment {deployment} -n production")
                    if not delete_deployment["success"]:
                        print(f"Failed to delete deployment {deployment}: {delete_deployment['error']}")

            services = run_script("kubectl get services -n production -o jsonpath='{.items[*].metadata.name}'")
            if not services["success"]:
                return {"success": False, "message": f"Failed to get services: {services['error']}"}

            services_list = services["output"].strip().split()
            for service in services_list:
                if service not in infra_repo:
                    delete_service = run_script(f"kubectl delete service {service} -n production")
                    if not delete_service["success"]:
                        print(f"Failed to delete service {service}: {delete_service['error']}")

        project_ids = get_ns()

        if not project_ids["success"]:
            return {"success": False, "message": "Failed to retrieve project IDs."}

        if len(project_ids["data"]) == 0:
            return {"success": True, "message": "No projects detected.", "results": []}

        results = []

        for project_id in project_ids["data"]:
            replacements = {'{{project_id}}': project_id}
            if infra_mode == "shared":
                script_path = 'script/shell/namespaces/delete-shared.sh'
            else:
                script_path = 'script/shell/namespaces/delete.sh'

            result = replace_and_run_shell(script_path, replacements)
            if result["success"]:
                results.append({"project_id": project_id, "message": f"Project {project_id} deleted successfully"})
            else:
                results.append({"project_id": project_id, "message": f"Failed to delete project {project_id}"})

        print("Finished restarting kube")  # Debug print
        return {"success": True, "results": results}

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
    
def create_redirect(project_id, project_domain, url_path, infra_mode):
    try:
        script_path = 'script/shell/ingress/redirect.sh'

        replacements = {'{{project_id}}': project_id, '{{infra_mode}}': infra_mode, '{{project_domain}}': project_domain, '{{url_path}}': url_path}
        
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
    
def delete_redirect(project_id):
    try:
        script_path = 'script/shell/ingress/delete-redirect.sh'

        replacements = {'{{project_id}}': project_id, '{{infra_mode}}': infra_mode}
        
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
    
def health_check(namespace):
    if infra_mode == "shared": 
        script_path = 'script/shell/namespaces/hc-shared.sh'
    else:
        script_path = 'script/shell/namespaces/hc.sh'

    replacements = {'{{namespace}}': namespace}
    
    # Run the script with the namespace dynamically replaced
    result = replace_and_run_shell(script_path, replacements)

    print(result)
    if not result['success']:
        return {"success": False, "message": result.get("error", "Unknown error occurred")}

    # Process the output to extract necessary details
    lines = result['output'].strip().split('\n')
    non_ready_deployments = []
    total_deployments = 0

    for line in lines:
        parts = line.split()
        if len(parts) < 2:
            continue
        total_deployments += 1
        deployment_name, ready_status = parts[0], parts[1]
        if ready_status == "False":
            non_ready_deployments.append(deployment_name)

    return {
        "success": True,
        "non_ready_deployments": non_ready_deployments,
        "total_deployments": total_deployments
    }

def change_mode(be_mode, infra_mode):
    script_path = 'script/shell/spin-up/change_mode.sh'

    replacements = {
        '{{github_pat}}': github_pat,
        '{{be_mode}}': be_mode,
        '{{infra_mode}}': infra_mode
    }

    results = []

    result = replace_and_run_shell(script_path, replacements)
    if result["success"]:
        results.append({"message": f"Change mode succesfully"})
    else:
        results.append({"message": f"Change mode failed"})

    return {"success": True, "data": results} if results else {"success": False, "data": [], "message": "No mode processed"}

def spin_up(be_mode):
    script_path = 'script/shell/spin-up/spin_up.sh'

    # Get both backend and frontend repositories
    repos_be = get_repos_be(be_mode)
    repos_fe = get_repos_fe()
    repos_infra = get_repos_infra()
    repos = repos_be + repos_fe + repos_infra

    results = []

    for repo in repos:
        replacements = {
            '{{github_pat}}': github_pat,
            '{{repo}}': repo
        }

        result = replace_and_run_shell(script_path, replacements)
        if result["success"]:
            results.append({"repo": repo, "message": f"Repo {repo} rerun successfully"})
        else:
            results.append({"repo": repo, "message": f"Failed to rerun repo {repo}. Error: {result.get('error')}"})

    return {"success": True, "data": results} if results else {"success": False, "data": [], "message": "No repos processed"}