import sqlite3 
#TODO: ADD Documentation later
class Calculations:
    def __init__(self, db_file):
        ''' 
        Initialize class variables
        :param db_file: The db file to be used by the class
        '''
        self.conn = self.create_connection(db_file)

    def create_connection(self,db_file):
        ''' 
        Creates a connection with the db
        :param db_file: The db file to create connection with
        '''
        conn = None 
        try: 
            conn = sqlite3.connect(db_file)
        except Error as e: 
            print(e)

        return conn

    def get_total_issues(self,conn):
        ''' 
        Returns the total number of issues
        :param conn: The db connection
        '''
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) from ISSUES ")
        result = cur.fetchall()[0][0]
        cur.close()
        return result

    def count_rows_by_col_value(self,col,value,conn):
        ''' 
        counts rows filtered by given column and specified value
        :param col: The column name
        :param value: The value for filtering
        :param conn: The db connection
        '''
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) {columnS} from ISSUES where {columnS}='{valueS}'".format(valueS=value,columnS=col))
        result = cur.fetchall()[0][0] # get first item in tuples
        cur.close()
        return result

    def get_open_count(self,conn):
        ''' 
        Returns the total number of open issues
        :param conn: The db connection
        '''
        open_count = self.count_rows_by_col_value("state","open",conn)
        return open_count

    def get_closed_count(self,conn):
        ''' 
        Returns the total number of closed issues
        :param conn: The db connection
        '''
        closed_count = self.count_rows_by_col_value("state","closed",conn)
        return closed_count

    def get_closed_to_open_ratio(self,conn):
        ''' 
        Returns the ratio of closed to opened issues
        :param conn: The db connection
        '''
        open_count = self.get_open_count(conn)
        closed_count = self.get_closed_count(conn)
        ratio = round((closed_count/ open_count),2)
        return ratio

    def get_closing_efficiency(self,conn):
        ''' 
        Returns efficiency, based on the principle of efficiency in physics, efficiency = output/input, where output = closed issues, input = total issues
        :param conn: The db connection
        '''
        total = self.get_total_issues(conn)
        closed_count = self.get_closed_count(conn)
        closing_efficiency = round((closed_count / total),2)
        closing_efficiency_percent = closing_efficiency * 100
        result = str(closing_efficiency_percent) + "%"
        return result

    def get_avg_days_to_close_issue(self,conn):
        ''' 
        Returns average number of days it takes to close an Issue
        :param conn: The db connection
        '''
        cur = conn.cursor()
        query = "SELECT julianday(closed_at) - julianday(created_at) from ISSUES where state='closed'"
        cur.execute(query)
        result = cur.fetchall()
        days = [i[0] for i in result]
        avg = round((sum(days) / len(days)),2)
        cur.close()
        return avg




        
    def __str__(self):
        opened = str(self.get_open_count(self.conn))
        closed = str(self.get_closed_count(self.conn))
        total = str(self.get_total_issues(self.conn))
        ratio = str(self.get_closed_to_open_ratio(self.conn))
        closing_efficiency = str(self.get_closing_efficiency(self.conn))
        average_close_time = str(self.get_avg_days_to_close_issue(self.conn))
        result = "Number of opened issues: " + opened + "\n"
        result += "Number of closed issues: " + closed + "\n"
        result += "Total number of issues: " + total + "\n"
        result += "Closed to open ratio: " + ratio + "\n"
        result += "closing_efficiency: " + closing_efficiency + "\n"
        result += "Average time taken to close issue: " + average_close_time + "\n"
        return result
    #TODO: Define tostring function, 

    #TODO: Issue maintainer response time
    #TODO: average days to close an issue

#test
A = Calculations("alt-tab-macos.db")
print(A)

        


