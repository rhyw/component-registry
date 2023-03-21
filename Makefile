DB_DATA_DIR:="db/dbdata/"
include .env

.PHONY: sync
sync:
	pip-sync requirements/dev.txt

build:
	. .env
	docker-compose build

.PHONY: redis
redis: corgi-db
	docker-compose -f db/docker-compose.yaml up corgi-redis

.PHONY: corgi-db
corgi-db:
	docker-compose -f db/docker-compose.yaml up corgi-db

.PHONY: stop-db
stop-db:
	docker-compose -f db/docker-compose.yaml down --remove-orphans

.PHONY: rmdb
rmdb: stop-db
	rm -fr $(DB_DATA_DIR)

.PHONY: hub
hub:
	# docker-compose -f docker-compose.yml up -d
	python manage.py migrate --settings config.settings.dev
	python manage.py runserver 0.0.0.0:9000 --settings config.settings.dev

.PHONE: clean
clean:
	docker container prune
	docker volume prune

.PHONE: up
up:
	docker-compose up corgi-web | tee debuginfo.log


.PHONE: dropdb
dropdb:
	docker-compose down
	docker volume rm component-registry_corgi-pg-data

.PHONE: down
down:
	docker-compose -f docker-compose.yml down

setup-ansible:
	$(ap) openshift/playbooks/local.yml -e ocp_namespace=corgi-stage -i openshift/inventory/corgi
deploy-stage:
	$(oc) project corgi-stage
	$(ap) openshift/playbooks/stage.yml -e ocp_token=$(ocptoken) --ask-vault-pass -e ocp_namespace=corgi-stage -i openshift/inventory/corgi

delete-stage-resources:
	$(oc) project corgi-stage
	$(oc) delete all --all
	$(oc) delete pvc --selector app=corgi-stage
