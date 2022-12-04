from wt_tree.Node import Node

class WaveletTree(object):

    def __init__(self, data=None, block_size=None):
        if data is None:
            print("Wavelet tree initialization error: Please give correct parameters")
            return
        self.__root = Node(data, block_size)  # Create the parent node

    """
    Query Functions
    """

    # if query string is N size, using N as position in rank_query,
    # finds out how many such chars exist in [0,N-1] string
    def rank_query(self, character=None, position=None):
        if character is None or position is None or position < 0:
            print("Rank error for: ", character, " for position: ", position, "Please give correct parameters")
            return -1
        return self.__root.get_rank_query(position, character)

    def rank_query_alt(self, character=None, position=None):
        if character is None or position is None or position < 0:
            print("Rank error for: ", character, " for position: ", position, "Please give correct parameters")
            return -1
        return self.__root.get_rank_query_alt(position, character)

    def select_query(self, character=None, position=None):
        if character is None or position is None or position <= 0:
            print("Select error for: ", character, " for position: ", position, "Please give correct parameters")
            return -1
        return self.__root.get_select_query(position, character)

    def track_symbol(self, position=None):
        if position is None or position <= 0:
            print("Track error for: ", position, "Please give correct parameters")
            return -1
        return self.__root.get_track_symbol(position)

    """
    Query Functions
    """
