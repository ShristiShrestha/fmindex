from wt_tree.Node import Node


class WaveletTree(object):

    def __init__(self, data=None, block_size=None):
        if data is None:
            print("Wavelet tree initialization error: Please give correct parameters")
            return
        self.__root = Node(data, None, block_size)  # Create the parent node

    def rank_query(self, character=None, position=None):
        if character is None or position is None or position < 0:
            print("Rank error for: ", character, " for position: ", position, "Please give correct parameters")
            return -1
        return self.__root.get_rank_query(position, character)
