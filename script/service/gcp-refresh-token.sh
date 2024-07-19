#!/bin/bash

# Check if the kubeconfig file exists and remove it if it does
if [ -f /root/.kube/config ]; then
  rm /root/.kube/config
fi

# Ensure the script is executed from the /app directory
cd /app

# Authenticate with the service account
gcloud auth activate-service-account --key-file=service-account/gcp.json

# Set the project
gcloud config set project antrein

# Get the GKE cluster credentials
gcloud container clusters get-credentials antrein-demo --zone asia-southeast1-a --project antrein
