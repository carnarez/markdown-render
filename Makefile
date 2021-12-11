.PHONY: build

style:
	/bin/bash build/style-highlight.sh > static/style-highlight.css

httpd:
	docker build --file build/Dockerfile.httpd --tag markdown-tests .

thttpd:
	docker build --file build/Dockerfile.thttpd --tag markdown-tests .

build: httpd

serve: build
	docker run --interactive --name www --publish 8000:80 --rm --tty markdown-tests
