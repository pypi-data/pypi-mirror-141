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
    _const_map: dict[str, MagicUrl]

    @classmethod
    def from_urls(cls, *args: str, **kwargs: str) -> "MagicUrlStore":
        """Create an entire store from a list of strings"""
        magic_urls = map(MagicUrl.from_str, args)

        const_map: dict[str, MagicUrl] = {}
        for name, url in kwargs.items():
            mu = MagicUrl.from_str(url)
            if mu._fragments:
                raise Exception(f"Not a constant url: '{url}' with name: '{name}'")
            const_map[name] = mu

        base_map: dict[str, MagicUrl] = {}
        for magic_url in magic_urls:
            fragments: str = ",".join(magic_url._fragments)
            if fragments in base_map:
                conflict_url = base_map[fragments]._url
                raise Exception(
                    f"Ambiguous fragments: {fragments} in '{magic_url._url}' and '{conflict_url}'"
                )
            base_map[fragments] = magic_url
        extended_map = {}
        for magic_url in base_map.values():
            frags: list[str] = list(magic_url._fragments.keys())
            for n in range(1, len(frags) + 1):
                key = ",".join(frags[:n])
                if key not in base_map:
                    extended_map[key] = magic_url
        full_map = extended_map | base_map
        return cls(full_map, base_map, const_map)

    def apply(self, _name: Optional[str] = None, **kwargs: str) -> str:
        """Applies a fragment map to the correct MagicUrl or gets
        unfragmentized url by name"""
        if _name:
            return self._const_map[_name]._url
        key = ",".join(kwargs.keys())
        url = self._map[key]
        return url.apply(**kwargs)
