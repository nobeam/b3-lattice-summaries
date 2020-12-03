# NOTE: this file is out of date use doit instead (https://pydoit.org/)
.PHONY: build deploy elegant_simulation elegant_data index summary

build: index elegant_summary elegant_data

index:
	poetry run index

elegant_summary: elegant_data
	poetry run elegant_summary

elegant_data: elegant_simulation
	poetry run elegant_data

elegant_simulation: $(patsubst lattices/%.lte, _simulations/elegant/%.twi, $(wildcard lattices/*.lte))

_simulations/elegant/%.twi: lattices/%.lte elegant/twiss.ele
	mkdir -p _simulations/elegant
	elegant elegant/twiss.ele -macro=energy=2500,lattice=$<,filename=$@ > /dev/null

.ONESHELL:
deploy: build
	cd dist
	git init
	git add -A
	git commit -m 'deploy'
	git push -f git@github.com:nobeam/b3.git master:gh-pages
	cd -
