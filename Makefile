.PHONY: build deploy twiss plots index summary 

build: index summary
	echo build ...

index:
	poetry run index

summary: plots
	poetry run summary

plots: twiss
	poetry run plots

twiss: $(patsubst lattices/%.lte, elegant_output/%.twi, $(wildcard lattices/*.lte))

elegant_output/%.twi: lattices/%.lte
	mkdir -p elegant_output
	elegant twiss.ele -macro=energy=2500,lattice=$<,filename=$@ > /dev/null

.ONESHELL:
deploy: build
	cd dist
	git init
	git add -A
	git commit -m 'deploy'
	git push -f git@github.com:nobeam/b3.git master:gh-pages
	cd -
