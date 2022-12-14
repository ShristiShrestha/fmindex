import typing

SkewTriplet = tuple[int, int, int]
SkewTripletDict = dict[SkewTriplet, int]

# We only explicitly use this for the central sentinel,
# but it is the same for the terminal sentinel
SENTINEL = 0


def safe_idx(x: typing.Sequence[int], i: int) -> int:
    """Hack to get zero if we index beyond the end."""
    return SENTINEL if i >= len(x) else x[i]


def symbcount(x: typing.Sequence[int], asize: int) -> list[int]:
    """Count how often we see each character in the alphabet."""
    # This is what collections.Counter does, but we need the
    # alphabet to be sorted integers, so we do it manually.
    counts = [0] * asize
    for a in x:
        counts[a] += 1
    return counts


def cumsum(counts: typing.Sequence[int]) -> list[int]:
    """Compute the cumulative sum from the character count."""
    res, acc = [0] * len(counts), 0
    for i, k in enumerate(counts):
        res[i] = acc
        acc += k
    return res


def bucket_sort(x: typing.Sequence[int], asize: int,
                idx: list[int], offset: int = 0) -> list[int]:
    """Sort indices in idx according to x[i + offset]."""
    sort_symbs = [safe_idx(x, i + offset) for i in idx]
    counts = symbcount(sort_symbs, asize)
    buckets = cumsum(counts)
    out = [0] * len(idx)
    for i in idx:
        bucket = safe_idx(x, i + offset)
        out[buckets[bucket]] = i
        buckets[bucket] += 1
    return out


def radix3(x: typing.Sequence[int], asize: int, idx: list[int]) -> list[int]:
    """Sort indices in idx according to first three letters in x."""
    idx = bucket_sort(x, asize, idx, 2)
    idx = bucket_sort(x, asize, idx, 1)
    return bucket_sort(x, asize, idx)


def triplet(x: typing.Sequence[int], i: int) -> SkewTriplet:
    """Extract the triplet x[i:i+3] safely."""
    assert i < len(x), "Don't create empty triplets!"
    return (safe_idx(x, i), safe_idx(x, i + 1), safe_idx(x, i + 2))


def less(x: typing.Sequence[int], i: int, j: int, isa: dict[int, int]) -> bool:
    """Check if x[i:] < x[j:] using the inverse suffix array for SA12."""
    a, b = safe_idx(x, i), safe_idx(x, j)
    if a < b:
        return True
    if a > b:
        return False
    if i % 3 != 0 and j % 3 != 0:
        return isa[i] < isa[j]
    return less(x, i + 1, j + 1, isa)


def merge(x: typing.Sequence[int],
          sa12: list[int], sa3: list[int]
          ) -> list[int]:
    """Merge the suffixes in sorted sa12 and sa3."""
    # I'm using a dict here, but you can use a list with a little
    # arithmetic
    isa = {sa12[i]: i for i in range(len(sa12))}
    sa = []
    i, j = 0, 0
    while i < len(sa12) and j < len(sa3):
        if less(x, sa12[i], sa3[j], isa):
            sa.append(sa12[i])
            i += 1
        else:
            sa.append(sa3[j])
            j += 1
    sa.extend(sa12[i:])
    sa.extend(sa3[j:])
    return sa