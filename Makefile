httpd:
	@docker build --file Dockerfile.httpd --tag markdown-render/web .

thttpd:
	@docker build --file Dockerfile.thttpd --tag markdown-render/web .

build: httpd

serve: build
	@docker run --interactive \
	            --name markdown-render-web \
	            --publish 8000:80 \
	            --rm \
	            --tty \
	            markdown-render/web
