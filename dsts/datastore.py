from sqlite3 import connect, IntegrityError

class datastore:
        """ Datastore class stores results derived from suffix array """
	def __init__(self):
            """ Constructor, initialises the database """
            self.conn = connect(':memory:')
            self.cursor = self.conn.cursor()
            self.cursor.execute('''CREATE TABLE substrings (string tex, pos integer,
                                   PRIMARY KEY (string, pos));''')
        
        def store_duplicate_substring(self, string, pos):
            """ Stores substring and corresponding position in the database """
            try:
                self.cursor.execute('INSERT INTO substrings VALUES (?,?)', (string, pos))
            except IntegrityError:
                pass

        def get_duplicate_positions_as_dict(self):
            """ Get positions where duplicate strings start, along with dupplicate strings"""
            tmp = self.get_duplicates()
            tmp_dict = {}
            for sub_str, pos in tmp:
                try:
                    tmp_dict[pos].append(sub_str)
                except KeyError:
                    tmp_dict[pos] = [sub_str,]
            return tmp_dict

        def get_duplicate_substrings_as_dict(self):
            """ Get strings that appear more than once along with positions as a dictionary """
            tmp = self.get_duplicates()
            tmp_dict = {}
            for sub_str, pos in tmp:
                try:
                    tmp_dict[sub_str].append(pos)
                except KeyError:
                    tmp_dict[sub_str] = [pos,]
            return tmp_dict

        def get_duplicate_positions_and_largest_string_size(self):
            """ Get positions where duplicate strings start, with size of largest string"""
            self.cursor.execute('SELECT pos, max(length(string)) FROM substrings group by pos')
            return self.cursor.fetchall()

        def get_duplicates(self):
            """ Return repeating substrings along with where duplicate strings start """
            self.cursor.execute('SELECT string, pos FROM substrings order by string, pos')
            return self.cursor.fetchall()

        def get_duplicate_substrings_and_count(self):
            """ Return repeating substrings, along with the number of positions they appear """
            self.cursor.execute('SELECT string, count(pos) FROM substrings group by string')
            return self.cursor.fetchall()
        
        def get_substring_length_and_replicas(self):
            """ Returns lengths, no of replicas, and occurances for duplicate substrings """
            self.cursor.execute('''SELECT k, r, count(*) from (
                                          SELECT length(string) as k, count(pos) as r 
                                          from substrings
                                          group by string)
                                   group by k, r''')
            return self.cursor.fetchall()
        

