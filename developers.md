### Wavelet Tree


### Performance benchmarking

#### BWT

1. Text Input Vs Time

lets run bwt only for different size
- size ranges from 1MB, 2MB, 3MB, ... 10MB 
- time profiling : measure diff between start and end time


2. Text Input Vs Memory consumed
Not sure about this

#### WT

1. text Input Vs Time (WT creation)

lets run WT creation only for different size
- size ranges from 1MB, 2MB, 3MB, ... 10MB 
- time profiling : measure diff between start and end time

2. Patten Input Vs Time (Rank Query)

lets run rank query on WT using proportionaly constant pattern size (e.g. for text 10000 chars pattern is 100 (0.001), 
so same goes for 5000 chars use pattern of size 50 ) , proportionally constant block size

3. Text Input Vs Memory used (WT creation)

lets run WT creation different input text and different block size we can use grouped bar graph


PRIORITIZE 1 & 3


#### func Node.__decode_data() - How does left and right nodes are decided from an array of chars?
1. Let's say `full_data` refers to all chars received during initialization. Either it could be whole text
in case the node is parent, or substring of BWT passed down by the parent node. 
2. Let's say `data` refers to unique chars in `full_data`
3. Now, sort `data` using its ASCII integer value in ascending order 
4. Split `data` into two halves (use positional index), less than half are false and more than half are true
5. From 4, split if done in `data`, boolean values are stored in `bits_data`
6. From 4, split if done in `full_data`, boolean values are stored in `bits_full_data`
7. **Conclusion** for each node, we complete two main tasks
    - calculate bit array for the node
    - determine which part of bit array in the node goes to either left or right children

#### func Node.__create_RRR() - How does each node enables rank, access, and select query?



