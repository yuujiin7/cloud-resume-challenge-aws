SHELL:=/bin/bash

.PHONY: build
.SILENT: integration-test
AWS_REGION := us-east-1
AWS_ACCOUNT_ID := 447447069092
REPOSITORY_NAME := my-resume-website-jiin-v1
IMAGE_NAME := cloud-resume-image
TAG := latest




build:
	sam build

create-json-config:
	HOSTED_ZONE=$$(aws-vault exec my-user --no-session -- aws route53 list-hosted-zones | jq .HostedZones[0].Id | cut -d "\"" -f 2 | cut -d "/" -f3); \
	DOMAIN_NAME=$$(aws-vault exec my-user --no-session -- \
		aws route53 list-resource-record-sets \
				--hosted-zone $$HOSTED_ZONE | \
				jq '.ResourceRecordSets[] | select(.Type == "NS") | .Name ' | \
				cut -d "\"" -f2 \
				| sed 's/.$$//'); \
	echo "{ \"HOSTED_ZONE\": \"$$HOSTED_ZONE\", \"DOMAIN_NAME\": \"$$DOMAIN_NAME\"  }" > config.json

integration-test:
	DOMAIN_NAME=$$(cat config.json | jq .DOMAIN_NAME -r); \
	FIRST=$$(curl -s "https://api.$$DOMAIN_NAME/get" | jq ".count| tonumber"); \
	curl -s "https://api.$$DOMAIN_NAME/put"; \
	SECOND=$$(curl -s "https://api.$$DOMAIN_NAME/get" | jq ".count| tonumber"); \
	echo "Comparing if first count ($$FIRST) is less than (<) second count ($$SECOND)"; \
	if [[ $$FIRST -le $$SECOND ]]; then echo "PASS"; else echo "FAIL";  fi

end-to-end-test:
	node end-to-end-test/index.js

deploy-infra:
	HOSTED_ZONE=$$(cat config.json | jq .HOSTED_ZONE -r); \
	DOMAIN_NAME=$$(cat config.json | jq .DOMAIN_NAME -r); \
	make build; \
	aws-vault exec my-user --no-session -- \
		sam deploy \
			--no-confirm-changeset \
			--parameter-overrides HostedZoneParameter=$$HOSTED_ZONE DomainNameParameter=$$DOMAIN_NAME

deploy-site:
	DOMAIN_NAME=$$(cat config.json | jq .DOMAIN_NAME -r); \
	sed -i '' "s/.eugenereycarta.*\.live/.$$DOMAIN_NAME/" resume-site/index.html; \
	aws-vault exec my-user --no-session -- aws s3 sync ./resume-site s3://my-resume-website-jiin-v1

hostedzone:
	aws-vault exec my-user --no-session -- aws route53 list-hosted-zones | jq .HostedZones[0].Id | cut -d "\"" -f 2 | cut -d "/" -f3

invoke-get:
	sam build && aws-vault exec my-user --no-session -- sam local invoke GetFunction

invoke-put:
	sam build && aws-vault exec my-user --no-session -- sam local invoke PutFunction

login:
	@aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

build:
	@docker build -t $(IMAGE_NAME) .

tag:
	@docker tag $(IMAGE_NAME):latest $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(REPOSITORY_NAME):$(TAG)

push: login
	@docker push $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com/$(REPOSITORY_NAME):$(TAG)

run:
	@docker run -p 9000:80 $(IMAGE_NAME):latest