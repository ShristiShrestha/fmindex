class Fmindex:
    def __init__(self, bwt_list):
        self.bwt_list = bwt_list
        self.dict = {}
        self.create_dict()

    def create_dict(self):
        self.dict = {}
        sorted_BWT = sorted(self.bwt_list)
        for char in set(sorted_BWT):
            self.dict[char] = sorted_BWT.index(char)

    def match(self, pattern, wavelet_tree, bwt_len):
        s = 0  # 0
        e = bwt_len
        for i in range(len(pattern) - 1, -1, -1):
            if pattern[i] in self.dict.keys():
                # if query string is N size, using N as position in rank_query,
                # finds out how many such chars exist in [0,N-1] string
                # So, for s = 0; count char in [0,-1] basically 0 return
                # similarly, for s=4 ; count char in [0, 3] here 3 index is counted (if it has char)
                # similarly, e = bwt_len; count char in [0, bwt_len - 1]

                # acc to blog, here rank query expects count value
                # up to (including) positions s and e
                s = self.dict[pattern[i]] + wavelet_tree.rank_query(pattern[i], s)
                e = self.dict[pattern[i]] + wavelet_tree.rank_query(pattern[i], e)
                if s > e:
                    return 0
            else:
                return 0
        count = e - s
        return count
