#!/bin/bash

# Set the project_id and base_url_create variables
project_id={{project_id}}
base_url_create={{base_url_create}}

# Debugging: Print the values of the variables to verify
echo "project_id: $project_id"
echo "base_url_create: $base_url_create"

script_path=script/k8s/ingress

# Use sed to replace placeholders for project_id and base_url
sed -e "s/<project_id>/$project_id/g" -e "s/<base_url>/$base_url_create/g" "$script_path.yml" > "$script_path-$project_id-temp.yml"

# Debugging: Print the temporary file content to verify replacements
cat "$script_path-$project_id-temp.yml"

# Apply the temporary ingress file
kubectl apply -f "$script_path-$project_id-temp.yml" || { echo "Failed to apply Ingress"; exit 1; }

# Optionally, remove the temporary file after applying
rm "$script_path-$project_id-temp.yml"
