from typing import Tuple

from faker.providers import BaseProvider

localized = True

PlaceType = Tuple[str, str, str, str, str, str, str, str]


class Provider(BaseProvider):
    peaks: Tuple[PlaceType, ...]
