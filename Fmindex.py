class Fmindex:
    def __init__(self, bwt_list):
        self.bwt_list = bwt_list
        self.dict = {}
        self.create_dict()

    def getDict(self):
        """
        this function returns a dictionary of each character in the alphabet
         with its rank in the alphabet. this is derived from the BWT and
          is used in calculating the FM-index
        """
        C_dict = {"$": 0}
        look_up = {}
        # simply count unique chars in O(n)
        for char in set(self.bwt_list):
            if char in C_dict.keys():
                C_dict[char] = 0
            else:
                C_dict[char] += 1
                #todo:

    def create_dict(self):
        self.dict = {}
        sorted_BWT = sorted(self.bwt_list)
        for char in set(sorted_BWT):
            self.dict[char] = sorted_BWT.index(char)

    def match(self, pattern, wavelet_tree, bwt_len):
        s = 1
        e = bwt_len
        for i in range(len(pattern) - 1, -1, -1):
            if pattern[i] in self.dict.keys():
                s = self.dict[pattern[i]] + wavelet_tree.rank_query(pattern[i], s - 1) + 1
                e = self.dict[pattern[i]] + wavelet_tree.rank_query(pattern[i], e)
                if s > e:
                    return 0
            else:
                return 0

        count = e - s + 1
        return count
