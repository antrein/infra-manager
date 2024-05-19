#!/bin/bash
PROJECT_ID={{project_id}}
CLUSTER_NAME={{cluster_name}}
ZONE={{zone}}


# Authenticate gcloud with the service account
gcloud auth activate-service-account --key-file=service-account/gcp.json

# Configure gcloud project and get GKE credentials
gcloud config set project $PROJECT_ID
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE --project $PROJECT_ID