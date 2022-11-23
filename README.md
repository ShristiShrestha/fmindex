Wavelet Tree
========

### References 
Reference for the ([Wavelet Tree](http://alexbowe.com/wavelet-trees/)).

Reference for the ([Node-RRR](http://alexbowe.com/wavelet-trees/)) of the Wavelet Tree. 

### Algorithm

###### Rank query
`Reporting the number of occurrences of a given character in a given prefix of the text.`
###### Select query
`Reporting the position of a given occurrence of a given character.`
###### Track symbol
`Reporting the character of a given position.`

### Code

```python
import sys
from FileReader import FileReader
from WaveletTree import WaveletTree

file_reader = FileReader(sys.argv)
if (not file_reader.is_read()):
    sys.exit()
wavelet_tree = WaveletTree(file_reader.get_letter())
wavelet_tree.rank_query(character, position)
wavelet_tree.select_query(character, position)
wavelet_tree.track_symbol(position)
```
