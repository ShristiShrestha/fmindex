# 3 blocks in each super block
# MUST make it dynamic like full_data_size // log2(full_data_size)
BLOCKS_NUM = 3

# size of a block in
# terms of number of bits it has
# MUST make it dynamic to the size of chars
# in the node like log2(full_data_size)
BITS_NUM = 5

# number of super blocks a node can have is 3+1
SUPER_BLOCK_SIZE = 3


class Node(object):
    '''
    classdocs
    '''

    def __init__(self, data=None, parent=None, from_left_parent=None, block_size=None):
        '''
        Constructor
        '''
        if data is None:
            print("Please give correct parameters")
            return
        self.full_data = data
        self.data = list(set(data))  # builds an array of unique elements from full_data
        self.data.sort(key=None, reverse=False)  # cmp=None removed SHRISTI SHRESTHA
        self.bits_data = []
        self.bits_full_data = []
        self.childern = []
        self.parent = parent
        self.from_left_parent = from_left_parent
        self.rs = []
        self.rb = []

        self.__decode_data()
        # self.__create_RRR()

        # counter for 1s for every block in the node
        self.block_ends = []
        self.block_size = block_size

        # count 1s in interval of block_size
        self.__create_block_ends()

        if self.__size() <= 1:
            return

        self.__gen_tree()

    """
    Query Functions
    """

    def get_rank_query(self, position=None, character=None):
        if self.__full_size() < position:
            return -1
        bit = self.__get_bit(character)
        position_size = self.__get_rank(position, bit)  # Calculate the rank
        # if this node is leaf, in that case
        # position_size will have value position - rank, and it is problematic
        # since chars in leaf node are the number of that chars in the whole string
        # so if this node is left leaf node, position_size = position - rank = 0
        # how? position equals the size of current node's full bits array
        # and that whole full data array is same chars in case of leaf node
        # therefore the above query __get_rank will return 0 for left leaf node
        if len(self.bits_data) == 1 and position_size == 0:
            return position - position_size  # position - (position - rank)
        if len(self.childern) < 1:  # When there are no children, return its rank
            return position_size
        if bit:  # For true(1) go to the right child, for false(0) go to the left child
            return self.childern[1].get_rank_query(position_size, character)
        return self.childern[0].get_rank_query(position_size, character)

    def get_rank_query_alt(self, position=None, character=None):
        if self.__full_size() < position:
            return -1
        bit = self.__get_bit(character)
        position_size = self.__get_rank_from_block_ends(position, bit)  # Calculate the rank
        # if this node is leaf, in that case
        # position_size will have value position - rank, and it is problematic
        # since chars in leaf node are the number of that chars in the whole string
        # so if this node is left leaf node, position_size = position - rank = 0
        # how? position equals the size of current node's full bits array
        # and that whole full data array is same chars in case of leaf node
        # therefore the above query __get_rank will return 0 for left leaf node
        if len(self.bits_data) == 1 and position_size == 0:
            return position - position_size  # position - (position - rank)
        if len(self.childern) < 1:  # When there are no children, return its rank
            return position_size
        if bit:  # For true(1) go to the right child, for false(0) go to the left child
            return self.childern[1].get_rank_query_alt(position_size, character)
        return self.childern[0].get_rank_query_alt(position_size, character)

    def get_select_query(self, position=None, character=None):
        leaf = self.__get_leaf(character)  # Get the leaf where the character is
        return leaf.__get_select(position, leaf.bits_data[leaf.data.index(character)])

    def get_track_symbol(self, position=None):
        if self.__size() == 2:  # When the size is 2 then i find leaf and must finish
            return self.full_data[position - 1]
        if self.__full_size() < position:
            return -1
        bit = self.bits_full_data[position - 1]
        position_size = self.__get_rank(position, bit)  # Calculate the rank

        if bit:  # For true(1) go to the right child, for false(0) go to the left child
            return self.childern[1].get_track_symbol(position_size)
        return self.childern[0].get_track_symbol(position_size)

    """
    Query Functions
    """
    """
    Private Functions
    """

    def __get_select(self, position=None, bit=None):
        curent_position = self.__find_position(position, bit)  # Find how many bit has the word until the position
        if self.parent == None:  # If is parent then find the position
            return curent_position
        if self.from_left_parent:  # For left child calculate False(0), for right child calculate True(1)
            return self.parent.__get_select(curent_position, False)
        return self.parent.__get_select(curent_position, True)

    def __find_position(self, position=None, bit=None):
        # position_size = self.__get_rank(position, bit)
        # curent_position = position#self.__get_rank(position, bit)
        # position_size = curent_position
        # if position_size == position:
        #    return curent_position
        position_size = 0
        curent_position = 1
        for d in self.bits_full_data:  # [position : self.__full_size()]:    #
            if d == bit:
                position_size += 1
            if position_size == position:
                return curent_position
            curent_position += 1
        return -1

    # rank refers to count of a char appearing before position
    # (excluding position), so basically how many times that char
    # appear before that position. However, instead of char, we inspect bit.
    # A bit can be 0 or 1. So, rank gives no of that bit (either 0 or 1)
    # appearing before position (again! excluding position's bit)
    def __get_rank(self, position=None, bit=None):
        if position is None or bit is None:
            print("Please give correct parameters")
            return -1

        # Initially it was only / that resulted in error
        # index cannot be a float, must be an integer
        # MUST - make sure position is localized correctly

        # e.g. if position 10 then BLOCKS_NUM (3) * BITS_NUM (5) = 15
        rs_position = position // (BLOCKS_NUM * BITS_NUM)  # eq 1; 0 number of (BLOCKS_NUM*BITS_NUM)
        rb_position = position // BITS_NUM  # eq 2; 2 i.e. number of BITS_NUM times

        # index out of range error for dna.txt
        rank = self.rs[rs_position]

        # Now, Check if the position is at the same area, if is then ignore the rb

        # first and condn is already covered by self.rs[rs_position] above

        # second and cond is true when rb_position is not multiple of BLOCKS_NUM as it
        # is already covered by self.rs[rs_position] above,
        # think abt it by substituting BITS_NUM from eq2 into eq 1
        # or when u r in first super block which is index 0
        if (((position % (BLOCKS_NUM * BITS_NUM)) != 0)
                and (((rs_position * BLOCKS_NUM) != rb_position) or (rs_position == 0))):
            rank += self.rb[rb_position]
        # Calculate the remaining bits
        last_position = (BITS_NUM * rb_position)
        while last_position < position:
            value = self.bits_full_data[last_position]
            if value:
                rank += 1
            last_position += 1

        # So rank is the number of 1s, so when you go left number of 0s is (total - num of 1s)
        if bit:  # If i look for True(1) okay return, if i look for False(0) then return the position - rank
            return rank
        return position - rank

    def __get_rank_from_block_ends(self, position=None, bit=None):
        rank = 0
        if position is None or bit is None:
            print("Please give correct parameters")
            return -1
        rb_position = position // self.block_size
        # ONLY A HACK METHOD
        rb_normalized = rb_position if rb_position < len(self.block_ends) else rb_position - 1
        rank = self.block_ends[rb_normalized]
        # better approach
        # if (rb_position == 0) or ((rb_position * self.block_size) != position):
        #     rank = self.block_ends[rb_position]

        last_position = self.block_size * rb_position
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
            return self.childern[1].__get_leaf(character)
        return self.childern[0].__get_leaf(character)

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
        self.__add_child(Node(left, self, True, self.block_size))  # left child is 0 index
        self.__add_child(Node(right, self, False, self.block_size))  # right child is 1 index

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
        self.childern.append(obj)

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

    #
    # self.block_ends stores no of 1s count in every block
    # e.g. [1, 4] -> from 0 to (block_size - 1) there is 1 number of 1s
    # and from block_size to (2*block_size - 1) there are 4 number of 1s
    # pattern for counter -> 1,2,3,4,1,2,3,4 incase block_size is 5
    def __create_block_ends(self):
        counter = 0
        rb_counter = 0
        num_blocks = 0

        self.block_size = 5 if self.block_size is None else self.block_size

        # by default 1 block has 0 1s
        self.block_ends.append(rb_counter)

        for data in self.bits_full_data:
            # periodically append cumulative count in each block
            # each block_end stores count for block_size bits upto that
            # position in the strings (within that node)
            if ((counter % self.block_size) == 0) and (counter != 0):
                self.block_ends.append(rb_counter)
                num_blocks += 1
            if data:
                rb_counter += 1
            counter += 1

        # few bits may have been left but not included in a block
        rem_for_new_block = rb_counter - self.block_ends[len(self.block_ends) - 1]
        if rem_for_new_block > 0:
            self.block_ends.append(rb_counter)

    # Create the RRR Node that make the rank very fast
    # We have to implement blocking may be here
    # at the end of each block, store count in that block
    def __create_RRR(self):
        counter = 0
        num_of_super_block = 0
        num_of_block = 0
        rs_counter = 0
        rb_counter = 0
        self.rb.append(rb_counter)
        # Calculate how many True(1) have in current Node,
        # to calculate the rs and rb.
        # rs is for the super block and
        # rb is for the block ;
        for data in self.bits_full_data:
            # BITS_NUM = 5; after every 5 chars, append block count
            # also increase number of blocks
            if ((counter % BITS_NUM) == 0) and (counter != 0):
                self.rb.append(rb_counter)
                num_of_block += 1

            # BLOCKS_NUM=3; BITS_NUM=5 ==> 15
            # after every 15 chars, append super block count
            # also increase number of super blocks
            if counter % (BLOCKS_NUM * BITS_NUM) == 0:
                self.rs.append(rs_counter)
                num_of_super_block += 1
                rb_counter = 0

            if data:
                rs_counter += 1
                rb_counter += 1

            counter += 1

        # count since last super block; remember on every new superblock creation
        # rb-counter is rest to 0
        self.rb.append(rb_counter)

        # what if number of super blocks is more than 4 since
        # SUPER_BLOCK_SIZE is 3
        while num_of_super_block < SUPER_BLOCK_SIZE + 1:
            self.rs.append(rs_counter)
            num_of_super_block += 1

    """
    Private Functions
    """
