.PHONY: all zip vendor clean mypy pylint fix
all: zip

PACKAGE_NAME := pinyin_translator

zip: $(PACKAGE_NAME).ankiaddon

$(PACKAGE_NAME).ankiaddon: src/*
	rm -f $@
	find src/ -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete
	rm -rf src/meta.json
	( cd src/; zip -r ../$@ * )

# TODO: certainly, there is a better way than this...
vendor:
	./venv/Scripts/pip install -r requirements.txt -t src/vendor

fix:
	python -m black src --exclude=vendor
	python -m isort src --skip=vendor

mypy:
	python -m mypy src

pylint:
	python -m pylint src

clean:
	rm -f $(PACKAGE_NAME).ankiaddon
