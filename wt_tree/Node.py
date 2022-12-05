class Node(object):

    def __init__(self, data=None, parent=None, block_size=None):
        if data is None:
            print("Please give correct parameters")
            return
        self.full_data = data
        self.data = list(set(data))  # builds an array of unique elements from full_data
        self.data.sort(key=None, reverse=False)  # cmp=None removed SHRISTI SHRESTHA
        self.bits_data = []
        self.bits_full_data = []
        self.children = []
        self.parent = parent

        self.__decode_data()

        # counter for 1s for every block in the node
        self.sub_blocks = []
        self.block_size = block_size

        # count 1s in interval of block_size
        self.__create_sub_blocks()

        if self.__size() <= 1:
            return

        self.__gen_tree()

    def get_rank_query(self, position=None, character=None):
        if self.__full_size() < position:
            return -1
        bit = self.__get_bit(character)
        position_size = self.__get_rank_from_sub_blocks(position, bit)  # Calculate the rank
        if len(self.children) < 1:  # When there are no children, return its rank
            return position_size
        if bit:  # For true(1) go to the right child, for false(0) go to the left child
            return self.children[1].get_rank_query(position_size, character)
        return self.children[0].get_rank_query(position_size, character)

    def __get_rank_from_sub_blocks(self, position=None, bit=None):
        rank = 0
        if position is None or bit is None:
            print("Please give correct parameters")
            return -1
        rb_position = position // self.block_size
        rb_normalized = rb_position if rb_position < len(self.sub_blocks) else rb_position - 1
        rank = self.sub_blocks[rb_normalized]
        # some bits might have been missed
        last_position = self.block_size * rb_normalized
        while last_position < position:
            value = self.bits_full_data[last_position]
            if value:
                rank += 1
            last_position += 1
        # So rank is the number of 1s, so when you go left number of 0s is (total - num of 1s)
        if bit:  # If i look for True(1) okay return, if i look for False(0) then return the position - rank
            return rank
        return position - rank

    def __get_leaf(self, character):  # Get the leaf where the character is
        index = self.data.index(character)
        if self.__size() == 2:
            return self
        value = self.bits_data[index]
        if value:
            return self.children[1].__get_leaf(character)
        return self.children[0].__get_leaf(character)

    def __gen_tree(self):  # Generate left and right child
        left = []
        right = []
        index = 0
        for data in self.bits_full_data:  # The True(1) got to the right and the False(0) go to the left
            if data:
                right.append(self.full_data[index])
            else:
                left.append(self.full_data[index])
            index += 1
        self.__add_child(Node(left, self, self.block_size))  # left child is 0 index
        self.__add_child(Node(right, self, self.block_size))  # right child is 1 index

    def __decode_data(self):  # Decode the data
        while len(self.bits_data) != self.__size():
            if len(self.bits_data) < self.__size() / 2:
                self.bits_data.append(False)
            else:
                self.bits_data.append(True)
        self.__set_bits()

    # based on unique chars boolean value,
    # update them for full data as well
    def __set_bits(self):  # set the full bit
        for char_item in self.full_data:
            # get bool for char_item from data bits
            # (remember data chars are unique chars)
            index = self.data.index(char_item)
            bit = self.bits_data[index]
            self.bits_full_data.append(bit)

    # Append the child. index 0 is the left, and 1 is right
    def __add_child(self, obj):
        self.children.append(obj)

    def __size(self):
        return len(self.data)

    def __full_size(self):
        return len(self.full_data)

    # Given a character return if is True(1) or False(0)
    def __get_bit(self, character=None):
        if character is None:
            return character
        # MAY BE: isn't data sorted ?, then use binary search for O(logk)
        # Complexity - O(k) where k is the length of
        # unique elements array in the node
        for data in self.data:
            if character == data:
                return self.bits_data[self.data.index(data)]
        return None

    # self.sub_blocks stores no of 1s count in every block
    # e.g. [1, 4] -> from 0 to (block_size - 1) there is 1 number of 1s
    # and from block_size to (2*block_size - 1) there are 4 number of 1s
    # pattern for counter -> 1,2,3,4,1,2,3,4 incase block_size is 5
    def __create_sub_blocks(self):
        counter = 0
        rb_counter = 0
        num_blocks = 0

        self.block_size = 5 if self.block_size is None else self.block_size

        # by default 1 block has 0 1s
        self.sub_blocks.append(rb_counter)

        for data in self.bits_full_data:
            # periodically append cumulative count in each block
            # each block_end stores count for block_size bits upto that
            # position in the strings (within that node)
            if ((counter % self.block_size) == 0) and (counter != 0):
                self.sub_blocks.append(rb_counter)
                num_blocks += 1
            if data:
                rb_counter += 1
            counter += 1

        # few bits may have been left but not included in a block
        rem_for_new_block = rb_counter - self.sub_blocks[len(self.sub_blocks) - 1]
        if rem_for_new_block > 0:
            self.sub_blocks.append(rb_counter)
