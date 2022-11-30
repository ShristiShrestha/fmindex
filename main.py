import sys

from BWT import BWT
from FileReader import FileReader
from Fmindex import Fmindex
from WaveletTree import WaveletTree


def main():
    texts = ["abracadra", "aaabbccccbba"]
    patterns = [["ab", "a", "/n"], ["aaab", "ds", "bb", "\\n"], ["m", "ss", "pp", "i", "ii", "B"]]

    # file_reader = FileReader("./short_text.txt")
    # if not file_reader.is_read():
    #     sys.exit()

    for index, text in enumerate(texts):
        (bwt, diff_seconds) = BWT(text).get_bwt()
        fmindex = Fmindex(bwt)
        bwt_chars = [char for char in bwt]
        wavelet_tree = WaveletTree(bwt_chars)
        print("String ", text)
        for pat in patterns[index]:
            print("Pattern: ", pat, ": ", fmindex.match(pat, wavelet_tree, len(bwt)))
    # (bwt, diff_seconds) = BWT(file_reader.get_text()).get_bwt()
    # fmindex = Fmindex(bwt)
    # bwt_chars = [char for char in bwt]
    # wavelet_tree = WaveletTree(bwt_chars)
    # for pat in patterns:
    #     print("Pattern: ", pat, ": ", fmindex.match(pat, wavelet_tree, len(bwt)))


if __name__ == '__main__':
    main()
