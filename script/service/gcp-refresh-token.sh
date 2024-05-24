#!/bin/bash

rm /root/.kube/config

# Authenticate with the service account
gcloud auth activate-service-account --key-file=service-account/gcp.json

# Set the project
gcloud config set project antrein-ta

# Get the GKE cluster credentials
gcloud container clusters get-credentials antrein --zone asia-southeast1-a --project antrein-ta