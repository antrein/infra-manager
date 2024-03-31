#!/bin/bash
project_id={{project_id}}

script_path=script/k8s/ingress

# Use sed to replace placeholders
sed -e "s/<project_id>/$project_id/g" "$script_path.yml" > "$script_path-$project_id-temp.yml"

# Apply the temporary ingress file
kubectl apply -f "$script_path-$project_id-temp.yml" || { echo "Failed to apply Ingress"; exit 1; }

# Optionally, remove the temporary file after applying
rm "$script_path-$project_id-temp.yml"