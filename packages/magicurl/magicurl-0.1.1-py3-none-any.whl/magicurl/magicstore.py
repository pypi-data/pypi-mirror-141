from typing import Optional

import operator
import re

from attrs import define

from .magicurl import MagicUrl


@define
class MagicUrlStore:
    """Storage for multiple MagicUrls"""

    _map: dict[str, MagicUrl]
    _base_map: dict[str, MagicUrl]

    @classmethod
    def from_urls(cls, *args: str) -> "MagicUrlStore":
        """Create an entire store from a list of strings"""
        magic_urls = map(MagicUrl.from_str, args)
        base_map: dict[str, MagicUrl] = {}
        for url in magic_urls:
            fragments: str = ",".join(url._fragments)
            if fragments in base_map:
                conflict_url = base_map[fragments]._url
                raise Exception(
                    f"Ambiguous fragments: {fragments} in '{url._url}' and '{conflict_url}'"
                )
            base_map[fragments] = url
        extended_map = {}
        for url in base_map.values():
            frags: list[str] = list(url._fragments.keys())
            for n in range(1, len(frags) + 1):
                key = ",".join(frags[:n])
                if key not in base_map:
                    extended_map[key] = url
        full_map = extended_map | base_map
        return cls(full_map, base_map)

    def apply(self, **kwargs: str) -> str:
        """Applies a fragment map to the correct MagicUrl"""
        key = ",".join(kwargs.keys())
        url = self._map[key]
        return url.apply(**kwargs)
