#!/bin/bash
project_id={{project_id}}

# Use sed to replace placeholders
sed -e "s/<project_id>/$project_id/g" "script/k8s/ingress.yml" > "script/k8s/ingress-temp-$project_id.yml"

# Apply the temporary ingress file
kubectl apply -f "script/k8s/ingress-temp-$project_id.yml" || { echo "Failed to apply Ingress"; exit 1; }

rm "script/k8s/ingress-temp-$project_id.yml"