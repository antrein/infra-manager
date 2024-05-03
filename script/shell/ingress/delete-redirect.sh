#!/bin/bash
project_id={{project_id}}
infra_mode={{infra_mode}}

if [[ "$infra_mode" == "shared" ]]; then
    kubectl -n production delete deployment gateway-proxy-$project_id
    kubectl -n production delete service gateway-proxy-$project_id
    kubectl -n production delete ingress gateway-proxy-$project_id
else
    kubectl -n $project_id delete deployment gateway-proxy
    kubectl -n $project_id delete service gateway-proxy
    kubectl -n $project_id delete ingress gateway-proxy
fi