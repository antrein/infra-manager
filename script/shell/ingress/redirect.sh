#!/bin/bash
project_id={{project_id}}
project_domain={{project_domain}}
url_path={{url_path}}

script_path=script/k8s/redirect

# Use sed to replace placeholders for project_id and project_domain
sed -e "s|<project_id>|$project_id|g" -e "s|<url_path>|$url_path|g" -e "s|<project_domain>|$project_domain|g" "$script_path.yml" > "$script_path-$project_id-temp.yml"

# Apply the temporary ingress file
kubectl apply -f "$script_path-$project_id-temp.yml" || { echo "Failed to apply Ingress"; exit 1; }

# Optionally, remove the temporary file after applying
rm "$script_path-$project_id-temp.yml"
