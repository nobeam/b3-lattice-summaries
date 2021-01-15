# Bessy III lattice summaries

Install lattice-data dependencies into new virtual environment:

```
poetry install
```

To generate data from lattices, the lattices are needed: set simlink to lattice-summaries-lattices

```
rm -rf lattices
ln -s ../lattice-summaries-lattices lattices
```

You may to use this variable to use the right mpl backend

```
export MPLBACKEND=SVG
```

Run all simulations and generate simulation output in directory `results`:

```
poetry run doit
```

or for indiviual lattices

```
poetry run doit ...(TODO FelixAndreas)
```


###########
## OLD from here - update ##
## Add a new lattice

The lattices are stored in the `lattices` directory. If you add an lattice, please add it to the `lattices/info.toml` file. Then create a pull requests.

## Build website

### Requirements

* Python 3.8 and Poetry (to manage dependencies)
* elegant
* git (used to deploy the website)

### Build

Run

```sh
make build

```

to build the website. The result will be stored in the `dist` folder.

## Deploy the website

Run

```sh
make deploy 
```

to deploy the website to Github Pages.
