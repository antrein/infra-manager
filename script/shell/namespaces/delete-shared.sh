project_id={{project_id}}
label="gateway-proxy-$project_id"

kubectl delete deployments -n production $label

# Delete services
kubectl delete services -n production $label

# Delete ingress
kubectl delete ingress -n production $label