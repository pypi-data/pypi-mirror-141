from typing import Optional

import operator
import re

from attrs import define


@define
class MagicUrl:
    """Stores a fragmentized URL
    e.g. https://example.org/{category}/{item}
    where 'category' and 'item' are fragments"""

    _url: str
    _fragments: dict[str, tuple[int, int]]

    @classmethod
    def from_str(cls, url: str) -> "MagicUrl":
        """Creates MagicUrl from a string"""
        parens_matcher = re.compile(r"{(.*?)}")
        fragments: dict[str, tuple[int, int]] = {}
        for match in parens_matcher.finditer(url):
            name = match.group(1)
            span = match.span()
            if name in fragments:
                raise Exception(f"Duplicate fragments in {url}")
            fragments[name] = span
        return MagicUrl(url, fragments)

    def apply(self, **kwargs: str) -> str:
        """Apply framgment map to MagicUrl"""
        apply_dict: dict[str, Optional[str]] = dict.fromkeys(self._fragments, None)
        result = self._url

        # mypy :/
        v: Optional[str] = None
        for k, v in kwargs.items():
            apply_dict[k] = v

        found_value = False
        for k, v in reversed(apply_dict.items()):
            if v is None:
                # gap found
                if found_value:
                    raise Exception(
                        "Fragments must be applied left to right with no gapps in between!"
                    )
                continue

            # found first value
            if not found_value:
                found_value = True
                # cut tail
                _, end = self._fragments[k]
                result = result[:end]

            # replace
            start, end = self._fragments[k]
            head = result[:start]
            tail = result[end:]
            result = head + v + tail
        return result
