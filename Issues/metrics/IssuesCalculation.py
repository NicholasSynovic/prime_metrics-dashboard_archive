import sqlite3 
# import pandas as pd
# db_file = "alt-tab-macos.db"
# conn = sqlite3.connect(db_file)
# decide if to use sql or pandas for the calculations
# df = pd.read_sql_query("select state from ISSUES", conn)
#TODO: ADD Documentation later
# cur = conn.cursor()
# cur.execute("SELECT COUNT(*) state from ISSUES where state='closed'")
# print(cur.fetchall()[0][0])


class Calculations:
    def __init__(self, db_file):
        # self.db_file = db_file
        self.conn = self.create_connection(db_file)

    def create_connection(self,db_file):
        conn = None 
        try: 
            conn = sqlite3.connect(db_file)
        except Error as e: 
            print(e)

        return conn

    def count_rows_by_col_value(self,col,value,conn):
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) {columnS} from ISSUES where {columnS}='{valueS}'".format(valueS=value,columnS=col))
        result = cur.fetchall()[0][0] # get first item in tuples
        return result

    def get_open_count(self,conn):
        open_count = self.count_rows_by_col_value("state","open",conn)
        return open_count

    def get_closed_count(self,conn):
        closed_count = self.count_rows_by_col_value("state","closed",conn)
        return closed_count

    def get_issues_effiency(self,conn):
        open_count = self.get_open_count(conn)
        closed_count = self.get_closed_count(conn)
        issues_efficiency = open_count / closed_count
        return issues_efficiency

        


#test
A = Calculations("alt-tab-macos.db")
print(A.get_open_count(A.conn))
print(A.get_closed_count(A.conn))
print(A.get_issues_effiency(A.conn))

        


