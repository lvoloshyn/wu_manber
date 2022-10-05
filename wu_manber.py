# -*- coding: utf-8 -*-

from collections import defaultdict
from typing import List, Tuple


class WuManber:
    B = 2

    def __init__(self, patterns: List[str]) -> None:
        self.patterns = patterns
        self.pattern_to_id = {pattern: i for i, pattern in enumerate(self.patterns)}

        self.m = self.get_min_pattern_length()
        self.shift_table = self.generate_shift_table()

        self.hash_table = defaultdict(list)
        self.prefix_table = defaultdict(list)

        for pattern in self.patterns:
            prefix = pattern[:self.B]  # using only first m!
            self.prefix_table[prefix].append(pattern)

            suffix = pattern[self.B: self.m]  # using only first m!
            self.hash_table[suffix].append(pattern)

    def search(self, text: str) -> List[Tuple[str, int]]:
        result = []

        ix = self.m - 1
        length = len(text)

        while ix < length:
            hash_1 = text[ix - self.B + 1: ix + 1]

            shift = self.shift_table.get(hash_1, self.shift_table.get("*"))
            if shift == 0:
                # check for matching prefixes
                hash_2 = text[ix - self.m + 1:ix - self.m + 1 + self.B]

                possible_patterns = self.prefix_table.get(hash_2)

                if possible_patterns:
                    for pattern in possible_patterns:
                        target = text[ix - self.m + self.B + 1:]
                        candidate = pattern[self.B:]

                        if len(target) < len(candidate):
                            continue

                        the_same = True
                        for c1, c2 in zip(target, candidate):
                            if c1 != c2:
                                the_same = False
                                break

                        if the_same:
                            pattern_start = ix - self.m + 1
                            result.append((pattern, pattern_start))

                shift = 1

            ix += shift

        return result

    def get_min_pattern_length(self):
        return len(min(self.patterns, key=len))

    def generate_shift_table(self):
        keys = set()

        shift = {"*": self.m - self.B + 1}

        for pattern in self.patterns:
            for i in range(self.m - 1):
                part = pattern[i:i + self.B]

                if len(part) == self.B:
                    keys.add(part)

        for key in keys:
            shift[key] = self.m - self.B + 1

        for key in keys:
            for pattern in self.patterns:
                if key in pattern[:self.m]:
                    j = pattern[:self.m].index(key)
                    shift[key] = min(shift.get(key), self.m - j - self.B)

        return shift
