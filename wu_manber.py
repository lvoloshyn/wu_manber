from typing import Dict, Generic, List, Tuple, TypeVar, Union

T = TypeVar("T", str, bytes, List, Tuple)


class WuManberSearch(Generic[T]):
    def __init__(self, patterns: List[T]) -> None:
        self.patterns: List[T] = patterns
        self.pattern_to_id: Dict[T, int] = {
            pattern: i for i, pattern in enumerate(self.patterns)
        }

        self.m = self.__get_min_pattern_length()
        self.B = min(2, self.m)  # to support 1-element patterns

        self.shift_table: Dict[Union[T, None], int] = self.__generate_shift_table()
        self.prefix_table: Dict[T, List[T]] = self.__generate_prefix_table()

    def __get_min_pattern_length(self) -> int:
        return len(min(self.patterns, key=len))  # type: ignore

    def __generate_prefix_table(self) -> Dict[T, List[T]]:
        prefix_table: Dict[T, List[T]] = {}

        for pattern in self.patterns:
            prefix = pattern[: self.B]  # using only first m!
            if prefix not in prefix_table:
                prefix_table[prefix] = []

            prefix_table[prefix].append(pattern)

        return prefix_table

    def __generate_shift_table(self) -> Dict[Union[T, None], int]:
        keys = set()

        shift: Dict[Union[T, None], int] = (
            {None: self.m - self.B + 1} if self.B > 1 else {None: 0}
        )

        for pattern in self.patterns:
            for i in range(self.m - 1):
                part = pattern[i : i + self.B]

                if len(part) == self.B:
                    keys.add(part)

        for key in keys:
            shift[key] = self.m - self.B + 1

        for key in keys:
            for pattern in self.patterns:
                if key in pattern[: self.m]:
                    j = pattern[: self.m].index(key)
                    shift[key] = min(shift[key], self.m - j - self.B)

        return shift

    @staticmethod
    def get_longest_spans(
        spans: List[Tuple[Union[T, int], int, int]]
    ) -> List[Tuple[Union[T, int], int, int]]:
        # we assume spans are sorted
        span_to_pattern: Dict[Tuple[int, int], Union[T, int]] = {
            (span[1], span[2]): span[0] for span in spans
        }

        non_overlapping_spans: List[Tuple[int, int]] = []

        for labeled_span in spans:
            span: Tuple[int, int] = labeled_span[1:]
            if not non_overlapping_spans:
                non_overlapping_spans.append(span)

            else:
                if span[0] >= non_overlapping_spans[-1][1]:
                    non_overlapping_spans.append(span)

                else:
                    non_overlapping_spans[-1] = (
                        non_overlapping_spans[-1][0],
                        max(span[1], non_overlapping_spans[-1][1]),
                    )

        return [
            (span_to_pattern[span], span[0], span[1]) for span in non_overlapping_spans
        ]

    def search(
        self, sequence: T, only_longest: bool = False, return_pattern_id: bool = False
    ) -> List[Tuple[Union[T, int], int, int]]:
        result: List[Tuple[Union[T, int], int, int]] = []

        ix = self.m - 1
        length = len(sequence)

        while ix < length:
            hash_1 = sequence[ix - self.B + 1 : ix + 1]

            shift = self.shift_table.get(hash_1, self.shift_table[None])
            if shift == 0:
                # check for matching prefixes
                hash_2 = sequence[ix - self.m + 1 : ix - self.m + 1 + self.B]

                possible_patterns = self.prefix_table.get(hash_2)

                if possible_patterns:
                    for pattern in possible_patterns:
                        target = sequence[ix - self.m + self.B + 1 :]
                        candidate = pattern[self.B :]

                        if len(target) < len(candidate):
                            continue

                        the_same = True
                        for c1, c2 in zip(target, candidate):
                            if c1 != c2:
                                the_same = False
                                break

                        if the_same:
                            pattern_start = ix - self.m + 1
                            pattern_end = pattern_start + len(pattern)
                            if return_pattern_id:
                                result.append(
                                    (
                                        self.pattern_to_id[pattern],
                                        pattern_start,
                                        pattern_end,
                                    )
                                )

                            else:
                                result.append((pattern, pattern_start, pattern_end))

                shift = 1

            ix += shift

        if only_longest:
            return self.get_longest_spans(result)

        return result
