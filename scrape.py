import json
import sys
import io
import re
import requests
from datetime import timedelta
import requests_cache
from logging import basicConfig, getLogger

from bs4 import BeautifulSoup, Tag, NavigableString

# Using https://www.artsy.net/categories build a database of artists to their genomes

basicConfig(level="INFO")
logger = getLogger("requests_cache.examples")

session = requests_cache.CachedSession(
    cache_name="artsy_cache", backend="sqlite", expire_after=timedelta(days=60)
)  # expire_after 7 days


def scrape_gene(gene, url):

    print(" *", f"scrape_gene: {gene}")

    r = session.get(url)

    print()

    if r.status_code == requests.codes.ok:

        html = r.content
        soup = BeautifulSoup(html, "lxml")

        for div in soup.findAll("div", attrs={"class": "jkcvUH"}):
            for artist in div.findAll("div", attrs={"class": "Text-sc-18gcpao-0"}):
                print(artist)

    return {}


def scrape_genomes(url):

    print(" *", f"source categories from: {url}")

    r = session.get(url)

    if r.status_code == requests.codes.ok:

        html = r.content
        soup = BeautifulSoup(html, "lxml")

        db = {}

        for div in soup.findAll("div", attrs={"id": re.compile(".*subject-matter.*")}):
            for a in div.findAll("a"):
                link = f"https://www.artsy.net/{a['href']}"
                gene = a.text.strip()
                db[gene] = scrape_gene(gene, link)
                print(db)
                sys.exit(0)

        print(db)


if __name__ == "__main__":

    db = scrape_genomes("https://www.artsy.net/categories")

    if db:
        with io.open("database/genomes.json", "w", encoding="utf8") as f:
            f.write(json.dumps(db, ensure_ascii=False))
            print(" *", f"written {len(db)} records")
