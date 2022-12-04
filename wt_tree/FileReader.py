import sys

class FileReader(object):
    def __init__(self, _filename):
        self.character = []
        self.__read_file(_filename)

    # Read the txt file and create a list from character
    def __read_file(self, filename=None):
        if filename is None:
            return
        try:
            with open(filename) as f:
                while True:
                    c = f.read(1)
                    if not c:
                        print("Read %i character Successfully" % len(self.character))
                        break
                    if ord(c) == 10:
                        continue
                    self.character.append(str(c))
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    def get_characters(self):
        if len(self.character) == 0:
            return None
        return self.character

    def get_text(self):
        if len(self.character) == 0:
            return None
        return "".join(self.character)

    def is_read(self):
        if len(self.character) == 0:
            return False
        return True

if __name__ == '__main__':
    file_reader = FileReader(sys.argv)