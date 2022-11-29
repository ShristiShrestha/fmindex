import sys
import time
sys.path.append("./fmindex/src")
sys.path.append("./fmindex")
from Suffix_array import skew
from bwt import BWT,getDict
from text_generator import random_string
from WaveletTree import WaveletTree
from Fmindex import match

# string = random_string(10)
# string = "Peter_Piper_picked_a_peck_of_pickled_peppers$"
# print(string)
# res = skew(string)
# res.pop(0)
# print(res)
# for item in res:
#     print(string[item:])
# print("---------------------------------")
# res_bwt = BWT(string, res)
# print(res_bwt)
# wavelet_tree = WaveletTree(res_bwt)
# rank = wavelet_tree.rank_query("e", 45)
# print(rank)
# # getDict(res_bwt)
# print(getDict(res_bwt))


string = "ississippisdemfofmefoemefisipsispsipepdkeisssssssssssf7fytf76f76tf76f76f7yuhguoygoi"
sa = skew(string)
sa.pop(0)
bwtr = BWT(string, sa)
print(bwtr)
wavelet_tree = WaveletTree(bwtr)


dict = getDict(bwtr)
print(dict)
a = match("iss", bwtr, dict)
print(a)

# with open("./fmindex/src/tests/english.50MB") as file:
#     string_list = file.read()
# start = time.time()
# res = skew(string_list)
# res_bwt = BWT(string_list, res)
# end = time.time()
# print("done")
# print(end - start)
# print(res_bwt)