.PHONY: build run clean
ENV?=local

build:
	cp -r ../../protos protos
	docker build -t harambe-deployment-engine .
	rm -r protos

run:
	docker run --rm -it --name hde -e NODE_ENV=${ENV} -p 5050:8080 harambe-deployment-engine

clean:
	docker rmi harambe-deployment-engine