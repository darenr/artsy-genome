# artsy-genome
Artsy Artist to Genome scraper and Database

Using https://www.artsy.net/categories build a database of artists to their genomes

```bash
conda config --add channels conda-forge
conda update -n base -c defaults conda
conda update -n base conda
conda env create -f environment.yml
conda activate genome
# keep enviroment up to date
conda env update --file environment.yml --prune
```