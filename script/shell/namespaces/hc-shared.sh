#!/bin/bash

# Define the namespace
NAMESPACE="{{namespace}}"

# Use kubectl to print deployment names and their ready conditions
kubectl get deployment -n production --no-headers -o custom-columns="NAME:.metadata.name,READY:.status.conditions[?(@.type=='Available')].status" | grep $NAMESPACE
kubectl get certificate -n production --no-headers -o jsonpath="{range .items[*]}{.metadata.name}{'\t'}{range .status.conditions[?(@.type=='Ready')]}{.status}{end}{'\n'}{end}" | grep $NAMESPACE