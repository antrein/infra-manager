#!/bin/bash

# Define the GitHub token and API URL
GITHUB_TOKEN={{github_pat}}
REPO={{repo}}

API_URL="https://api.github.com/repos/antrein/$REPO/actions/runs?per_page=1"

# Fetch the latest workflow run
response=$(curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  $API_URL)

# Extract the rerun URL using jq
rerun_url=$(echo $response | jq -r '.workflow_runs[0].rerun_url')

# Rerun last run
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
"$rerun_url"