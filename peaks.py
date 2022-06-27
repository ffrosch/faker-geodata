import os
import pprint
from contextlib import redirect_stdout
from pathlib import Path
from typing import List

import geocoder
import requests
from dotenv import load_dotenv

load_dotenv()
key = os.environ.get("GEONAMES_USERNAME")

LANG = "de"
COUNTRY = "CH"

OUTFILE = f"data/peaks/{LANG}_{COUNTRY}.txt"


class Peak:
    def __init__(
        self,
        name="",
        countryName="",
        countryCode="",
        adminName1="",
        adminCode1="",
        lat="",
        lng="",
        **kwargs,
    ):
        self.name = name
        self.country = countryName
        self.country_code = countryCode
        self.state = adminName1
        self.state_code = adminCode1
        self.lat = lat
        self.lng = lng
        self.elevation = ""

    def __lt__(self, other):
        return self.name < other.name

    def to_tuple(self):
        return (
            str(self.name),
            str(self.country),
            str(self.country_code),
            str(self.state),
            str(self.state_code),
            str(self.lat),
            str(self.lng),
            str(self.elevation),
        )


def get_elevations(peaks: List[Peak]) -> List[str]:

    locations = ""
    for p in peaks:
        if len(locations):
            locations += "|"
        locations += f"{p.lat},{p.lng}"

    url = f"https://api.opentopodata.org/v1/eudem25m?locations={locations}"
    r = requests.get(url=url)
    results = r.json()["results"]
    elevations = [str(data["elevation"]) for data in results]

    return elevations


# https://geocoder.readthedocs.io/index.html
# https://www.geonames.org/export/geonames-search.html
data = geocoder.geonames(
    "Switzerland",
    key=key,
    country=COUNTRY,
    featureClass="T",
    maxRows=100,
    lang=LANG,
)


peaks = sorted([Peak(**peak.raw) for peak in data])
elevations = get_elevations(peaks)

for i, elev in enumerate(elevations):
    peaks[i].elevation = elev

Path(OUTFILE).parent.mkdir(parents=True, exist_ok=True)
with open(OUTFILE, "w") as f:
    with redirect_stdout(f):
        pp = pprint.PrettyPrinter(width=120, compact=True)
        pp.pprint(tuple(p.to_tuple() for p in peaks))
