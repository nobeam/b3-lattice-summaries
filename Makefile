# TODO: maybe it's better to use doit instead (https://pydoit.org/)
.PHONY: build deploy simulation_elegant elegant_data index

build: index summary_elegant data_elegant summary_apace data_apace

index:
	poetry run index

summary_elegant: data_elegant
	poetry run summary_elegant

data_elegant: simulation_elegant scripts/data_elegant.py
	poetry run data_elegant

simulation_elegant: $(patsubst lattices/%.lte, _simulations/elegant/%.twi, $(wildcard lattices/*.lte))

_simulations/elegant/%.twi: lattices/%.lte elegant/twiss.ele
	mkdir -p _simulations/elegant
	# TODO: make energy variable!
	elegant elegant/twiss.ele -macro=energy=2500,lattice=$<,filename=$@ > /dev/null

summary_apace: data_apace
	poetry run summary_apace

data_apace:  scripts/data_apace.py
	poetry run data_apace

# TODO: decide if elegant lattice files should be generated from latticejson
# elegant_lattices:  $(patsubst lattices/%.json, _simulations/elegant/%.lte, $(wildcard lattices/*.json))
#
# _simulations/elegant/%.lte: lattices/%.json
# 	mkdir -p _simulations/elegant
# 	latticejson convert --force --from json --to lte --stdout $< > $@

.ONESHELL:
deploy:
	rm -rf dist
	make build
	cd dist
	git init
	git add -A
	git commit -m 'deploy'
	git push -f git@github.com:nobeam/b3.git master:gh-pages
	cd -
