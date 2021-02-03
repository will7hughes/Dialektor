GCLOUD_PROJECT:=$(shell gcloud config list project --format="value(core.project)")

.PHONY: all
all: deploy

.PHONY: create-cluster
create-cluster:
	gcloud container clusters create dialektor-cluster \
		--scopes "https://www.googleapis.com/auth/userinfo.email","cloud-platform"

.PHONY: create-bucket
create-bucket:
	gsutil mb gs://$(GCLOUD_PROJECT)
	gsutil defacl set public-read gs://$(GCLOUD_PROJECT)

.PHONY: build
build:
	docker build -t gcr.io/$(GCLOUD_PROJECT)/dialektor .

.PHONY: push
push: build
	docker push -- gcr.io/$(GCLOUD_PROJECT)/dialektor

.PHONY: deploy
deploy: push 
	kubectl create -f deploy.yaml

.PHONY: update
update:
	kubectl patch deployment dialektor -p "{\"spec\":{\"template\":{\"metadata\":{\"labels\":{\"date\":\"`date +'%s'`\"}}}}}"

.PHONY: delete
delete:
	kubectl delete deployments dialektor
	kubectl delete service dialektor
