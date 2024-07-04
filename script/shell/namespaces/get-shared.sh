#!/bin/bash

# Print the header
echo "NAME"

# Fetch deployments from the 'production' namespace and process them to extract suffixes
kubectl get deployments -n production | awk '/gateway-proxy-/ { 
    if(NR > 1) {  # Skip the header row from the kubectl output
        split($1, a, "-");
        print a[3];  # Assuming the name format is gateway-proxy-suffix
    }
}'
