CLUSTER_NAME=aegis
CLUSTER_URL=http://127.0.0.1:50308/

cluster-create:
	kind create cluster --name $(CLUSTER_NAME) --image kindest/node:v1.23.5 --config=k8s/kind.yaml
	kubectl config current-context
	kubectl create sa python

cluster-delete:
	kind delete cluster --name $(CLUSTER_NAME)
	kind delete clusters $(CLUSTER_NAME)
	kind delete cluster --name kind-$(CLUSTER_NAME)
	kind delete clusters kind-$(CLUSTER_NAME)

cluster-auth:
	TOKENS=$(kubectl describe sa python | grep Tokens | awk '{print $2}')
	@echo "export KIND_TOKEN=$(kubectl get secret $(TOKENS) -o json | jq -r .data.token | base64 --decode)" >> .env
	curl -k -X GET -H "Authorization: Bearer $KIND_TOKEN" $(CLUSTER_URL)apis
	kubectl apply -f ./k8s/service-account/

auth:
	@echo "KIND_TOKEN=$$(kubectl get secret $$(kubectl describe sa python | grep Tokens | awk '{print $$2}') -o json | jq -r .data.token | base64 --decode)" >> token.txt
	
run:
	uvicorn main:app --reload

docker-build:
	docker build -t ta-infra-manager .

docker-run:
	docker run -dp 8000:8000 ta-infra-manager