SELL=/bin/bash

style:
	/bin/bash build/style-highlight.sh > static/style-highlight.css

build:
	docker build --file build/Dockerfile.httpd --tag www:markdown-tests .

serve: build
	docker run --interactive --name www --publish 8000:80 --rm --tty www:markdown-tests
