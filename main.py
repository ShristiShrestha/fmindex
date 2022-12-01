import sys

from BWT import BWT
from FileReader import FileReader
from Fmindex import Fmindex
from WaveletTree import WaveletTree


def main():
    texts = [
        "banana",
        "abracadra",
        "aaabbccccbba",
        "mississippi",
        "winningIsSoHappeningSeeForYourselfIseeItIsHappening"
    ]
    patterns = [
                ["b", "nan", "ana"],
                ["aba", "a", "/n"],
                ["aaab", "ds", "bb", "\\n"],
                ["m", "ss", "pp", "i", "ii", "B"],
                ["ing", "in", "ning", "win", "is"]]

    for index, text in enumerate(texts):
        (bwt, diff_seconds) = BWT(text).get_bwt()
        fmindex = Fmindex(bwt)
        bwt_chars = [char for char in bwt]
        wavelet_tree = WaveletTree(bwt_chars, 5)
        print("String ", text)
        for pat in patterns[index]:
            print("Pattern: ", pat, ": ", fmindex.match_alt(pat, wavelet_tree, len(bwt)))


if __name__ == '__main__':
    main()
