import time
import numpy
def create_sa(text):
    # construct s12
    s12_unsorted = create_s12(text)

    # sort s12 suffixes
    s12_with_ranks = bucketsort(text, s12_unsorted)
    s12_ranks = [value[0] for value in s12_with_ranks]

    if len(set(s12_ranks)) == len(s12_ranks):
        s12 = [value[1] for value in sorted(s12_with_ranks, key=lambda x: x[0])]
    else:
        sa_s12 = create_sa(s12_ranks)
        s12 = [s12_with_ranks[idx][1] for idx in sa_s12]

    # sort s0 suffix
    s0 = create_s0(text, s12)

    """ Task 2 - 1"""
    # create inverse sa
    inverse_sa = create_inverse_sa(len(text), s12)
    merged_sa = merge_sa(text, s0, s12, inverse_sa)
    return merged_sa


# construct s12
def create_s12(text):
    # creating the array
    s1 = []
    s2 = []

    # filling the triplet arrays
    for idx in range(len(text)):
        if (idx % 3) == 1:
            s1.append(idx)
        elif (idx % 3) == 2:
            s2.append(idx)
    return s1 + s2


# sort s12 suffixes

def bucketsort(current_text, sa, s0=False):
    triplet_idx = 2
    if s0:
        triplet_idx = 0
    sorted_sa = sa

    # sort the sa
    for i in range(triplet_idx, -1, -1):
        buckets = dict()

        for text_idx in sorted_sa:
            triplet = get_triplet(current_text, text_idx)
            checked_i = i if i < len(triplet) else len(triplet) - 1
            if triplet[checked_i] not in buckets:
                buckets[triplet[checked_i]] = []
            buckets[triplet[checked_i]].append(text_idx)
        sorted_sa = []
        for key in sorted(buckets.keys()):
            sorted_sa += buckets[key]
    # get the ranks
    ranks = dict()
    rank = 1

    for text_idx in sorted_sa:
        triplet = ''.join([str(x) for x in get_triplet(current_text, text_idx)])
        if triplet not in ranks:
            ranks[triplet] = rank
            rank += 1

    # combine s12 and ranks
    s12_with_ranks = [(ranks.get(''.join([str(x) for x in get_triplet(current_text, idx_original)])), idx_original) for
                      idx_original in sa]
    return s12_with_ranks

def get_triplet(text, idx):
    triplet = []
    for text_idx in range(idx, min(idx + 3, len(text))):
        triplet.append(text[text_idx])
    while len(triplet) < 3 and isinstance(triplet, str):
        triplet.append("$")
    return triplet


# sort s0 suffix
def create_s0(text, s12):
    s0_unsorted = []

    # create the s0 sorted by the second letter
    for idx_text in s12:
        if ((idx_text - 1) % 3) == 0:
            s0_unsorted.append(idx_text - 1)

    if len(text) % 3 == 1:
        s0_unsorted.insert(0, len(text) - 1)
    # sort the s0 - but only the by the first letter
    s0_with_ranks = bucketsort(text, s0_unsorted, s0=True)
    # extract the values for s0
    s0 = [x[1] for x in sorted(s0_with_ranks, key=lambda x: x[0])]
    return s0


"""
Task 2 - 1
- merge s0 and s12
- for this you need to create the inverse_sa
"""


# create the inverse sa for the merge
def create_inverse_sa(len_text, sa):
    inverse_sa = [-1] * len_text
    for sa_idx in range(len(sa)):
        inverse_sa[sa[sa_idx]] = sa_idx
    return inverse_sa


def merge_sa(text, s0, s12, inverse_sa):
    sa = []
    idx_s0 = 0
    idx_s12 = 0

    while (idx_s0 + idx_s12) < (len(s0) + len(s12)):
        if idx_s0 >= len(s0):
            sa.append(s12[idx_s12])
            idx_s12 += 1
            continue

        if idx_s12 >= len(s12):
            sa.append(s0[idx_s0])
            idx_s0 += 1
            continue

        current_s0 = s0[idx_s0]
        current_s12 = s12[idx_s12]

        # check for first char
        if text[current_s0] > text[current_s12]:
            sa.append(current_s12)
            idx_s12 += 1
            continue

        if text[current_s0] < text[current_s12]:
            sa.append(current_s0)
            idx_s0 += 1
            continue

        if text[current_s0] == text[current_s12]:
            i = 1
            while True:
                # check with inverse_sa
                if (current_s0 + i) % 3 == 0 or (current_s12 + i) % 3 == 0:
                    # check for second char
                    if text[current_s0 + i] > text[current_s12 + i]:
                        sa.append(current_s12)
                        idx_s12 += i
                        break

                    if text[current_s0 + i] < text[current_s12 + i]:
                        sa.append(current_s0)
                        idx_s0 += i
                        break

                    if text[current_s0 + i] == text[current_s12 + i]:
                        i += 1
                        continue
                    continue

                if inverse_sa[current_s0 + i] > inverse_sa[current_s12 + i]:
                    sa.append(current_s12)
                    idx_s12 += 1
                    break

                if inverse_sa[current_s0 + i] < inverse_sa[current_s12 + i]:
                    sa.append(current_s0)
                    idx_s0 += 1
                    break
    return sa

def create_bwt(text):
    seconds1 = time.time()
    # Finding suffix array
    sa = create_sa(text)
    bwt = ""
    # Combining index to find BWT
    for index in sa:
        bwt += text[index - 1]
    seconds2 = time.time()
    with open('./output/suffix_array_dna.txt', 'w') as f:
        f.write(str(sa))
    with open('bwt_dna.txt', 'w') as f:
        f.write(bwt)

    print("Time taken: ", seconds2 - seconds1)
    return bwt, seconds2 - seconds1

