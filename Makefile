.PHONY: build

style:
	/bin/bash utils/style-highlight.sh > style/style-highlight.css

httpd:
	@docker build --file build/Dockerfile.httpd --tag markdown-render/web .

thttpd:
	@docker build --file build/Dockerfile.thttpd --tag markdown-render/web .

build: httpd

serve: build
	@docker run --interactive \
	            --name markdown-render-web \
	            --publish 8000:80 \
	            --rm \
	            --tty \
	            markdown-render/web
