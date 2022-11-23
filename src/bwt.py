

def BWT(text: str, sa: list):
    """
    returns BWT of the given text  with respect to its Suffix Array
    """
    return list(text[i - 1] for i in sa)

def getDict(bwt_list):
    """
    this function returns a dictionary of of each character in the alphabet with its rank in the alphabet. this is derived from the BWT and is used in calculating the FM-index
    """
    C_dict = {}
    sorted_BWT=sorted(bwt_list)
    for char in set(sorted_BWT):
        C_dict[char] = sorted_BWT.index(char)
    return C_dict