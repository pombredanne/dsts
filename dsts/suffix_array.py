from pprint import pprint


class SuffixArray:
    def __init__(self, string_to_parse):
        """ Constructor, builds and sorts the array """
        self.str = string_to_parse
        self.suffix_array = []
        for i in range(len(self.str)):
            self.suffix_array.append(self.str[i:len(self.str)])
        self.suffix_array.sort()
        self.duplicates = {}
        self.duplicates_pos = {}
        self.duplicates_pos_lcp = {}
        self.repetitions = []
        
    def return_array_as_string(self):
        """ Return the contents of the array """
        tmp_str = ""
        for i in range(len(self.suffix_array)):
            tmp_str = tmp_str + "%s %s\n" % (i, self.suffix_array[i])
        return tmp_str
        
    def return_original_str(self):
        """ Returns the original string """
        return self.str

    def search(self, target):
        """ Searches the suffix array for substring using binary search on prefixes, returns first instance """
        lo = 0
        hi = len(self.str)
        pprint(self.suffix_array)
        while hi > lo:
            middle = (lo + hi) /2
            if target == self.suffix_array[middle][0:len(target)]:
                return self.get_pos(middle)
            elif target > self.suffix_array[middle][0:len(target)]:
                lo = middle + 1
            else:
                hi = middle
        return -1 # not found

    def get_pos(self, pos):
        """ Returns the position of the suffix array element in the original string """
        return len(self.str) - len(self.suffix_array[pos])

    def find_all_duplicates(self):
        """ Searches for all duplicate substrings """
        for i in range(len(self.suffix_array)-1,-1,-1): # for each item in suffix array counting backwards
            for j in range(len(self.suffix_array[i]),0,-1): # for each character in row counting backwards
                self.__search_backwards_for_suffix(i, j)
        
        for position in self.duplicates_pos:
            high = 0 # Use counter to keep track of largest length of string at given position
            tmp_str = "" # Use to keep track of largest string at given position
            for string in self.duplicates_pos[position]:
                # Record position where string occurs
                try:
                    self.duplicates[string].append(position) 
                except:
                    self.duplicates[string] = [position,]
                # Record where largest string occurs
                if high < len(string):
                    high = len(string)
                    tmp_str = string
            self.duplicates_pos_lcp[position] = tmp_str             

    def get_duplicate_substrings(self):
        """ Returns substrings that appear more than once along their positions """
        dict_tmp = {}
        for key in self.duplicates:
            dict_tmp[key] = list(self.duplicates[key])

        return dict_tmp

    def get_duplicate_positions(self,padding=False):
        """ Returns positions that are the starting position for duplicate substrings """
        return self.duplicates_pos

    def __search_backwards_for_suffix(self, sa_pos, endpoint):
        """ Searches for prefix backwards from given position
        sa_pos = position in suffix array where prefix string to be searched is located
        endpoint = terminating point for search prefix
        """
        string = self.suffix_array[sa_pos][:endpoint]
        i = sa_pos - 1 # Move pointer to row adjecent to the search parameter in suffix array
        if self.suffix_array[i].startswith(string): # prefix found
            # Keep track in each position what duplicate duplicated substrings appear
            try:
                self.duplicates_pos[self.get_pos(i)].append(string)
                self.duplicates_pos[self.get_pos(sa_pos)].append(string)
            except KeyError:
                self.duplicates_pos[self.get_pos(i)] = [string,]
                self.duplicates_pos[self.get_pos(sa_pos)] = [string,]
            # Keep track of duplicated substrings and where they appear in the original string
            #try:
            #    self.duplicates[string].add(self.get_pos(i))
            #    self.duplicates[string].add(self.get_pos(sa_pos))
            #except KeyError:
            #    self.duplicates[string] = Set([self.get_pos(i), self.get_pos(sa_pos)])
