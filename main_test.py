import sys

from FileReader import FileReader
from Fmindex import Fmindex
from WaveletTree import WaveletTree
from bwt_swagat import create_bwt

if __name__ == '__main__':

    file_reader = FileReader("dna.txt")
    if not file_reader.is_read():
        sys.exit()

    (bwt, diff_seconds) = create_bwt(file_reader.get_text() + "$")
    fmindex = Fmindex(bwt)
    bwt_chars = [char for char in bwt]
    wavelet_tree = WaveletTree(bwt_chars, 5)
    # print("Pattern: ", "ss", ": ", fmindex.match("ss", wavelet_tree, len(bwt_chars)))

    print("Pattern: ", "GCCAGG", ": ", fmindex.match_alt("GCCAGG", wavelet_tree, len(bwt_chars))) # 4872
