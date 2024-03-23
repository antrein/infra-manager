#!/bin/bash

project_id={{project_id}}
GIT_EMAIL="reyshazni@gmail.com"
GIT_USER="reyshazni"
GIT_TOKEN={{github_pat}}
BE_MODE={{be_mode}}

DIRECTORY="prod-yml-$project_id"
DEPLOYMENTS=("bc-dashboard" "bc-queue" "poc-fe")

cd "script/k8s/" || exit 1

# Configure git
git config --global user.email "$GIT_EMAIL"
git config --global user.name "$GIT_USER"

# Clone the repository with credentials
git clone "https://${GIT_USER}:${GIT_TOKEN}@github.com/antrein/prod-yml.git" "$DIRECTORY" || exit 1

# Iterate through each YAML file in the directory
for file in "$DIRECTORY"/"$BE_MODE"/*.yml; do
    # Use awk to replace 'namespace: production' with 'namespace: new'
    awk -v new_namespace="$project_id" '{gsub("namespace: production", "namespace: " new_namespace)}1' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done

# Apply the YAML files
kubectl apply -f "$DIRECTORY"/"$BE_MODE"/ || exit 1

# Remove the directory
rm -rf "$DIRECTORY/" || exit 1

echo "Deployment YAML files updated and folder removed successfully."
