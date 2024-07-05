#!/bin/bash

project_id={{project_id}}
project_domain={{project_domain}}
url_path={{url_path}}
infra_mode={{infra_mode}}
base_url={{base_url}}

GIT_EMAIL="reyshazni@gmail.com"
GIT_USER="reyshazni"
GIT_TOKEN={{github_pat}}
BE_MODE={{be_mode}}

DIRECTORY="gateway-proxy-$project_id"
REPO_URL="https://${GIT_USER}:${GIT_TOKEN}@github.com/antrein/prod-yml.git"
script_path=""

# Configure git
git config --global user.email "$GIT_EMAIL"
git config --global user.name "$GIT_USER"

# Clone the repository
git clone "$REPO_URL" "$DIRECTORY" || { echo "Failed to clone repository"; exit 1; }

# Determine script path based on infra_mode and copy the appropriate YAML file
if [[ "$infra_mode" == "shared" ]]; then
    script_path="script/k8s/redirect-shared"
    cp "$DIRECTORY/gateway-proxy/shared.yml" "$script_path.yml"
else
    script_path="script/k8s/redirect"
    cp "$DIRECTORY/gateway-proxy/multi.yml" "$script_path.yml"
fi

# Replace placeholders in the copied YAML file
sed -e "s|<project_id>|$project_id|g" \
    -e "s|<url_path>|$url_path|g" \
    -e "s|<project_domain>|$project_domain|g" \
    -e "s|<infra_mode>|$infra_mode|g" \
    -e "s|<base_url>|$base_url|g" \
    "$script_path.yml" > "$script_path-$project_id-temp.yml" || { echo "Failed to replace placeholders"; exit 1; }

# Apply the temporary ingress file
kubectl apply -f "$script_path-$project_id-temp.yml" || { echo "Failed to apply Ingress"; exit 1; }

# Clean up temporary files
rm "$script_path-$project_id-temp.yml"
rm -rf "$DIRECTORY"

if [[ "$infra_mode" == "shared" ]]; then
    rm "script/k8s/redirect-shared.yml"
else
    rm "script/k8s/redirect.yml"
fi

echo "Ingress for project $project_id applied successfully and temporary files cleaned up."
