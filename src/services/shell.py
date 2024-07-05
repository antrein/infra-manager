# src/services/shell.py
import subprocess

def run_shell(script_path):
    try:
        with open(script_path, 'r') as file:
            script = file.read()
        result = subprocess.run(script, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, executable='/bin/bash')
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None
    
def run_script(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return {"success": True, "output": result.stdout.decode('utf-8').strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.decode('utf-8').strip()}
    
def replace_and_run_shell(script_path, replacements):
    print(replacements)
    # Read the script file
    with open(script_path, 'r') as file:
        script_content = file.read()

    # Replace placeholders with actual values
    for placeholder, value in replacements.items():
        script_content = script_content.replace(placeholder, value)

    # Execute the modified script
    try:
        result = subprocess.run(
            ['/bin/bash', '-c', script_content], 
            check=False, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        return {"success": True, "output": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr.strip()}