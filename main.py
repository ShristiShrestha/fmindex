'''
Created on Jun 9, 2014

@author: nectarios
'''
import sys

from FileReader import FileReader
from WaveletTree import WaveletTree


def main():
    file_reader = FileReader("./input.txt")
    if not file_reader.is_read():
        sys.exit()
    wavelet_tree = WaveletTree(file_reader.get_characters())
    # print(wavelet_tree.track_symbol(1))
    print(wavelet_tree.rank_query('e', 45))
    # print(wavelet_tree.select_query('e', 1))


if __name__ == '__main__':
    main()
