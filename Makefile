SHELL=/bin/bash

.venv:
	@python3 -m venv .venv
	@.venv/bin/pip install -U pip
	@.venv/bin/pip install --no-cache-dir -r build/requirements.txt

style:
	@/bin/bash build/style-highlight.sh > static/style-highlight.css

tests: style .venv
	@.venv/bin/python render.py prose/markdown.md > index.html

build: style
	docker build --file build/Dockerfile --tag www .

serve: build
	docker run --name www --publish 8000:80 --rm www

clean:
	-@rm -fr index.html __pycache__ .venv
