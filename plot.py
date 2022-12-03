import tracemalloc
import sys
import time

from FileReader import FileReader
from Fmindex import Fmindex
from WaveletTree import WaveletTree
from bwt_swagat import create_bwt
from matplotlib import pyplot as plt

def plot(file, pattern):

    file_reader = FileReader(file)
    if not file_reader.is_read():
        sys.exit()

    (bwt, diff_seconds) = create_bwt(file_reader.get_text() + "$")
    fmindex = Fmindex(bwt)
    tracemalloc.start()

    bwt_chars = [char for char in bwt]
    BWTcurrent, BWTpeak = tracemalloc.get_traced_memory()
    print("BWT memory peak in MB:", BWTcurrent)
    tracemalloc.stop()
    timeList = []
    spaceList = []
    WTtimeLIst =  []
    for i in range(1, 21):

        tracemalloc.start()
        start0 = time.time_ns()
        wavelet_tree = WaveletTree(bwt_chars, i)
        end0= time.time_ns()
        WTtimeLIst.append(end0-start0)
        print("size of object: ", sys.getsizeof(wavelet_tree))
        current, peak = tracemalloc.get_traced_memory()
        peakMB = peak / (1024*1024)
        spaceList.append(peakMB)

        tracemalloc.stop()
        start1 = time.time_ns()
        fm = fmindex.match_alt(pattern, wavelet_tree, len(bwt_chars))
        print("Pattern: ", pattern, ": ", fm)
        end1 = time.time_ns()
        timeList.append(end1-start0)
        print(end1-start1)
        del wavelet_tree,current, peakMB, peak, fm
    
    f1 = plt.figure(1)
    plt.scatter([str(i) for i in range(1,21)],WTtimeLIst)
    plt.ylabel('WT creation time in ns')
    plt.xlabel('Number of Blocks in WT')

    f2 = plt.figure(2)
    plt.scatter([str(i) for i in range(1,21)],spaceList)
    plt.ylabel('WT creation memory usage in MB')
    plt.xlabel('Number of Blocks in WT')

    f3 = plt.figure(3)
    # plt.axis([0, 22, 389.030, 389.04])
    plt.scatter([str(i) for i in range(1,21)],timeList)
    plt.ylabel('Pattern matching runtime in ns')
    plt.xlabel('Number of Blocks in WT')
    plt.show()

plot("dna.txt", "AAGGA")
# plot("english.txt", "Chapter")
# plot("protein_data", "SGAPPPE")