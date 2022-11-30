import time

"""
Task 2 - 0
- construct s12
- sort s12 suffixes
- sort s0 suffix
"""

class BWT:
    def __init__(self, text):
        self.text = text + "$"
        self.bwt = ""

    def create_sa(self, current_text):
        """ Task 2 - 0 """
        # construct s12
        s12_unsorted = self.create_s12(current_text)

        # sort s12 suffixes
        s12_with_ranks = self.bucketsort(current_text, s12_unsorted)
        s12_ranks = [value[0] for value in s12_with_ranks]

        if len(set(s12_ranks)) == len(s12_ranks):
            s12 = [value[1] for value in sorted(s12_with_ranks, key=lambda x: x[0])]
        else:
            sa_s12 = self.create_sa(s12_ranks)
            s12 = [s12_with_ranks[idx][1] for idx in sa_s12]

        # sort s0 suffix
        s0 = self.create_s0(current_text, s12)

        """ Task 2 - 1"""
        # create inverse sa
        inverse_sa = self.create_inverse_sa(len(current_text), s12)
        merged_sa = self.merge_sa(current_text, s0, s12, inverse_sa)
        return merged_sa

    def create_s12(self, current_text):
        # creating the array
        s1 = []
        s2 = []

        # filling the triplet arrays
        for idx in range(len(current_text)):
            if (idx % 3) == 1:
                s1.append(idx)
            elif (idx % 3) == 2:
                s2.append(idx)
        return s1 + s2

    def bucketsort(self, current_text, sa, s0=False):
        triplet_idx = 2
        if s0:
            triplet_idx = 0
        sorted_sa = sa

        # sort the sa
        for i in range(triplet_idx, -1, -1):
            buckets = dict()

            for text_idx in sorted_sa:
                triplet = self.get_triplet(current_text, text_idx)
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
            triplet = ''.join([str(x) for x in self.get_triplet(current_text, text_idx)])
            if triplet not in ranks:
                ranks[triplet] = rank
                rank += 1

        # combine s12 and ranks
        s12_with_ranks = [(ranks.get(''.join([str(x) for x in self.get_triplet(current_text, idx_original)])), idx_original) for
                          idx_original in sa]
        return s12_with_ranks

    def get_triplet(self, current_text, idx):
        triplet = []
        for text_idx in range(idx, min(idx + 3, len(current_text))):
            triplet.append(current_text[text_idx])
        while len(triplet) < 3 and isinstance(triplet, str):
            triplet.append("$")
        return triplet

    def create_s0(self, current_text, s12):
        s0_unsorted = []

        # create the s0 sorted by the second letter
        for idx_text in s12:
            if ((idx_text - 1) % 3) == 0:
                s0_unsorted.append(idx_text - 1)

        if len(current_text) % 3 == 1:
            s0_unsorted.insert(0, len(current_text) - 1)
        # sort the s0 - but only the by the first letter
        s0_with_ranks = self.bucketsort(current_text, s0_unsorted, s0=True)
        # extract the values for s0
        s0 = [x[1] for x in sorted(s0_with_ranks, key=lambda x: x[0])]
        return s0

    def create_inverse_sa(self, len_text, sa):
        inverse_sa = [-1] * len_text
        for sa_idx in range(len(sa)):
            inverse_sa[sa[sa_idx]] = sa_idx
        return inverse_sa

    def merge_sa(self, current_text, s0, s12, inverse_sa):
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
            if current_text[current_s0] > current_text[current_s12]:
                sa.append(current_s12)
                idx_s12 += 1
                continue

            if current_text[current_s0] < current_text[current_s12]:
                sa.append(current_s0)
                idx_s0 += 1
                continue

            if current_text[current_s0] == current_text[current_s12]:
                i = 1
                while True:
                    # check with inverse_sa
                    if (current_s0 + i) % 3 == 0 or (current_s12 + i) % 3 == 0:
                        # check for second char
                        if current_text[current_s0 + i] > current_text[current_s12 + i]:
                            sa.append(current_s12)
                            idx_s12 += i
                            break

                        if current_text[current_s0 + i] < current_text[current_s12 + i]:
                            sa.append(current_s0)
                            idx_s0 += i
                            break

                        if current_text[current_s0 + i] == current_text[current_s12 + i]:
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

    def get_bwt(self):
        seconds1 = time.time()
        sa = self.create_sa(self.text)
        self.bwt = ""
        for index in sa:
            self.bwt += self.text[index - 1]
        seconds2 = time.time()
        return self.bwt, seconds2 - seconds1
