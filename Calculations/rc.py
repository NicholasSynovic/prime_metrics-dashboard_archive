import sqlite3
import sys
from sqlite3 import Connection, Cursor

from NewCalculations import Calculations


def main():
    db_file = sys.argv[1]
    calc = Calculations(db_file)
    conn = calc.create_connection(db_file)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS CALCULATIONS;")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS CALCULATIONS (calc_name VARCHAR(3000), value VARCHAR(3000));"
    )
    data = [
        ("Team Effort(secondss)", calc.get_team_effort(conn)),
        ("Issue density(issues/kloc)", calc.calculate_issue_density(conn)),
        ("closed to open ratio", calc.get_closed_to_open_ratio(conn)),
        ("closing efficiency (%)", calc.get_closing_efficiency(conn)),
        ("average days to close issues(days)", calc.get_avg_days_to_close_issue(conn)),
    ]
    sql = "insert into CALCULATIONS(calc_name,value) VALUES(?,?);"
    cursor.executemany(sql, data)
    conn.commit()
    # insert calculations into table
    print("Inserted calculations into table")


if __name__ == "__main__":
    main()
