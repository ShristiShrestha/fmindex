
import sys
import time

from BWT import BWT
from FileReader import FileReader
from Fmindex import Fmindex
from WaveletTree import WaveletTree
from SA_BWT import getBwt


texts = [
        "abracadra",
        "aaabbccccbba",
        "mississippi",
        "winningIsSoHappeningSeeForYourselfIseeItIsHappening"
    ]
# patterns = [["aba", "a", "/n"],
#                 ["aaab", "ds", "bb", "\\n"],
#                 ["m", "ss", "pp", "i", "ii", "B"],
#                 ["ing", "in", "ning", "win", "is"]]


patterns = ["AGGA","GGAAGGA", "AAGGA"]

# file_reader = FileReader("./dna.txt")
# if not file_reader.is_read():
#     sys.exit()

# for index, text in enumerate(texts):
#     (bwt, diff_seconds) = BWT(text).get_bwt()
#     fmindex = Fmindex(bwt)
#     bwt_chars = [char for char in bwt]
#     wavelet_tree = WaveletTree(bwt_chars)
#     print("String ", text)
#     print(bwt)
#     for pat in patterns[index]:
#         print("Pattern: ", pat, ": ", fmindex.match(pat, wavelet_tree, len(bwt)))

bwt = getBwt()
fmindex = Fmindex(bwt)
print("fm done")
print(time.time())
bwt_chars = [char for char in bwt]
wavelet_tree = WaveletTree(bwt_chars)
for pat in patterns:
    print("Pattern: ", pat, ": ", fmindex.match(pat, wavelet_tree, len(bwt)))