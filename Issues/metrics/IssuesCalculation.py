import sqlite3 
#TODO: ADD Documentation later
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

    def get_total_issues(self,conn):
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) from ISSUES ")
        result = cur.fetchall()[0][0]
        return result

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

    def get_closed_to_open_ratio(self,conn):
        open_count = self.get_open_count(conn)
        closed_count = self.get_closed_count(conn)
        ratio = round((open_count / closed_count),2)
        return ratio

    def get_closing_efficiency(self,conn):
        total = self.get_total_issues(conn)
        closed_count = self.get_closed_count(conn)
        closing_efficiency = round((closed_count / total),2)
        closing_efficiency_percent = closing_efficiency * 100
        result = str(closing_efficiency_percent) + "%"
        return result

        
    def __str__(self):
        opened = str(self.get_open_count(self.conn))
        closed = str(self.get_closed_count(self.conn))
        total = str(self.get_total_issues(self.conn))
        ratio = str(self.get_closed_to_open_ratio(self.conn))
        closing_efficiency = str(self.get_closing_efficiency(self.conn))
        result = "Number of opened issues: " + opened + "\n"
        result += "Number of closed issues: " + closed + "\n"
        result += "Total number of issues: " + total + "\n"
        result += "Closed to open ratio: " + ratio + "\n"
        result += "closing_efficiency: " + closing_efficiency
        return result
    #TODO: Define tostring function, 

    #TODO: Issue maintainer response time
    #TODO: average days to close an issue

#test
A = Calculations("alt-tab-macos.db")
print(A)
# print(A.get_open_count(A.conn))
# print(A.get_closed_count(A.conn))
# print(A.get_closed_to_open_ratio(A.conn))
# print(A.get_closing_efficiency(A.conn))

        


