.PHONY: build

style:
	/bin/bash build/style-highlight.sh > static/style-highlight.css

httpd:
	docker build --file build/Dockerfile.httpd --tag markdown-tests .

thttpd:
	docker build --file build/Dockerfile.thttpd --tag markdown-tests .

build: httpd

serve: build
	docker run --interactive --name www --publish 8000:80 --rm --tty \
	-v $(PWD)/static/style.css:/var/www/style.css \
	-v $(PWD)/static/style-markdown.css:/var/www/style-markdown.css \
	-v $(PWD)/static/style-search.css:/var/www/style-search.css \
	markdown-tests
