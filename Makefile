SHELL=/bin/bash

style:
	@/bin/bash build/style-highlight.sh > static/style-highlight.css

build: style
	docker build --file build/Dockerfile --tag www .

serve: build
	docker run --name www --publish 8000:80 --rm www
