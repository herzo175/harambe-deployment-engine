.PHONY: build run

build:
	docker build -t harambe-deployment-engine .

run:
	docker run --rm -it --name hde -p 3000:8080 harambe-deployment-engine