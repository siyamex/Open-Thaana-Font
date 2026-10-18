# Build OpenThaana-Regular from source.
# Requires: pip install -r requirements.txt

.PHONY: all build clean verify install-deps

all: build

install-deps:
	pip install -r requirements.txt

build:
	python build.py

verify:
	python -c "import build; build.verify()"

clean:
	rm -rf fonts/ build/ instance_ufo/ master_ufo/
