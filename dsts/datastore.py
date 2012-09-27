#!/usr/bin/env python

# Defines class necessary for suffix array persistance

from sqlite3 import connect, IntegrityError

create_tables_sql = """
CREATE TABLE IF NOT EXISTS substrings (string text, pos integer, PRIMARY KEY (string, pos));
CREATE TABLE IF NOT EXISTS suffix_array (suffix integer);
CREATE TABLE IF NOT EXISTS data (key string, value string, PRIMARY KEY (key, value));
"""


class datastore:
    """ Datastore class stores results derived from suffix array """
    def __init__(self, operation=None, filename=None):
        """ Constructor, initialises the database """

        if not operation:
            self.conn = connect(':memory:')
        elif operation == 'load':
            self.conn = connect(filename)
        elif operation == 'save':
            self.conn = connect(filename)
        self.cursor = self.conn.cursor()
        self.cursor.executescript(create_tables_sql)

    def store_duplicate_substring(self, string, pos):
        """ Stores substring and corresponding position in the database """
        if not isinstance(string, unicode):
            string = unicode(string, errors='ignore')
        try:
            self.cursor.execute('INSERT INTO substrings VALUES (?,?)', (string, pos))
            self.conn.commit()
        except IntegrityError:
            pass

    def save_suffix_array(self, suffix_array, doc):
        """ Save suffix array into the database """
        if not isinstance(doc, unicode):
            doc = unicode(doc, errors='ignore')
        for line in suffix_array:
            self.cursor.execute('INSERT INTO suffix_array VALUES (?)', (line,))
        self.cursor.execute("INSERT INTO data VALUES ('document', ?)", (doc,))
        self.conn.commit()

    def load_suffix_array(self):
        """ Load suffix array into the database """
        suffix_array = []
        self.cursor.execute('SELECT suffix FROM suffix_array')
        [suffix_array.append(line[0]) for line in self.cursor.fetchall()]
        return suffix_array

    def load_document(self):
        """ Load complete string from database """
        self.cursor.execute("SELECT value from data where key = 'document'")
        return self.cursor.fetchone()[0]

    def get_duplicate_positions_as_dict(self):
        """ Get positions where duplicate strings start, along with duplicate strings"""
        tmp = self.get_duplicates()
        tmp_dict = {}
        for sub_str, pos in tmp:
            try:
                tmp_dict[pos].append(sub_str)
            except KeyError:
                tmp_dict[pos] = [sub_str, ]
        return tmp_dict

    def get_duplicate_substrings_as_dict(self):
        """ Get strings that appear more than once along with positions as a dictionary """
        tmp = self.get_duplicates()
        tmp_dict = {}
        for sub_str, pos in tmp:
            try:
                tmp_dict[sub_str].append(pos)
            except KeyError:
                tmp_dict[sub_str] = [pos, ]
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

    def get_distinct_substring_length_and_replicas(self):
        """ Returns lengths, no of replicas, and occurances for duplicate substrings """
        self.cursor.execute('SELECT k, r, count(*) from '
                            '(SELECT length(string) as k, count(pos) as r '
                            'from substrings group by string) group by k, r')
        return self.cursor.fetchall()

    def get_substring_length_and_replicas(self):
        """ Returns lengths and no of replicas for duplicate substrings """
        self.cursor.execute('SELECT length(string), count(pos) from substrings group by string')
        return self.cursor.fetchall()

    def close(self):
        """ Closes the connection to the database """
        self.cursor.close()
