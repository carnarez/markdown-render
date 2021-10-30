SHELL=/bin/bash

.venv:
	@python3 -m venv .venv
	@.venv/bin/pip install -U pip
	@.venv/bin/pip install --no-cache-dir -r requirements.txt

css:
	@/bin/bash style-highlight.sh > style-highlight.css

test: .venv css
	@.venv/bin/python render.py markdown.md > index.html

build:
	docker build --tag www .

serve: build
	docker run --name www --publish 8000:80 --rm www

clean:
	-@rm -fr index.html __pycache__ .venv
