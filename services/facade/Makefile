.PHONY: build run clean

build:
	docker build -t harambe-deployment-engine .

run:
	docker run --rm -it --name hde -e NODE_ENV=local -p 5050:8080 harambe-deployment-engine

clean:
	docker rmi harambe-deployment-engine