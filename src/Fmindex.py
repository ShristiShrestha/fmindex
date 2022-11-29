import sys
sys.path.append("./fmindex")
from WaveletTree import WaveletTree

def match(patern, bwt, dict):
    """
  fmIndex using bwt and a dictionary of sorted charachters in the input
    """
    count = 0
    s = 2
    e = len(bwt)
    wavelet_tree = WaveletTree(bwt)
    for i in range(len(patern) - 1, -1, -1):
       
        s = dict[patern[i]] + wavelet_tree.rank_query(patern[i], s-1) + 1
        e = dict[patern[i]] + wavelet_tree.rank_query(patern[i], e)
        if s > e:
            return False
    
    count = e - s + 1
    return count