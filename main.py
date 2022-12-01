import sys
import time
# from memory_profiler import profile

from BWT import BWT
from SA_BWT import getBwt
from FileReader import FileReader
from Fmindex import Fmindex
from WaveletTree import WaveletTree


def main():
    # texts = [
    #     "abracadra",
    #     "aaabbccccbba",
    #     "mississippi",
    #     "winningIsSoHappeningSeeForYourselfIseeItIsHappening"
    # ]
    # patterns = [["aba", "a", "/n"],
    #             ["aaab", "ds", "bb", "\\n"],
    #             ["m", "ss", "pp", "i", "ii", "B"],
    #             ["ing", "in", "ning", "win", "is"]]

    texts = "abracadra"
    patterns = "c"


    (bwt, diff_seconds) = getBwt(texts)
    print(bwt)
    fmindex = Fmindex(bwt)
    bwt_chars = [char for char in bwt]
    wavelet_tree = WaveletTree(bwt_chars)
    print("String ", texts)
    
    print("Pattern: ", patterns, ": ", fmindex.match(patterns, wavelet_tree, len(bwt)))

    # file_reader = FileReader("./dna.txt")
    # if not file_reader.is_read():
    #     sys.exit()

    # for index, text in enumerate(texts):
    #     (bwt, diff_seconds) = getBwt(text)
    #     fmindex = Fmindex(bwt)
    #     bwt_chars = [char for char in bwt]
    #     wavelet_tree = WaveletTree(bwt_chars)
    #     print("String ", text)
    #     for pat in patterns[index]:
    #         print("Pattern: ", pat, ": ", fmindex.match(pat, wavelet_tree, len(bwt)))
    
    
    
    # input =file_reader.get_text()

    # (bwt, diff_seconds) = getBwt(input)
    # print(diff_seconds)
    # fmindex = Fmindex(bwt)
    # bwt_chars = [char for char in bwt]
    # start = time.time()
    # wavelet_tree = WaveletTree(bwt_chars)
    # end = time.time()
    # print("WT creation:", end - start)
    # for pat in patterns:
    #     print("Pattern: ", pat, ": ", fmindex.match(pat, wavelet_tree, len(bwt)))


if __name__ == '__main__':
    main()
