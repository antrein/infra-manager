# src/logic/kubernetes.py
from src.services.shell import replace_and_run_shell, run_shell
from dotenv import load_dotenv, dotenv_values


load_dotenv()
config = dotenv_values(".env")

cloud_platform = config["CLOUD_PLATFORM"]

gcp_project_id = config["GCP_PROJECT_ID"]
gcp_cluster_name = config["GCP_CLUSTER_NAME"]
gcp_zone = config["GCP_ZONE"]

def refresh_kubectl_token():
    if cloud_platform == "gcp":
        script_path = 'script/service/gcp-refresh-token.sh'
        
        # Run the script with the namespace dynamically replaced
        result = run_shell(script_path)

        print(result)
        if not result['success']:
            return {"success": False, "message": result.get("error", "Unknown error occurred")}

        return {
            "success": True,
        }
    else:
        return {
            "success": True,
        }