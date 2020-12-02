# Bessy III lattice summaries

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
