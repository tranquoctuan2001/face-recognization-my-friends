import sqlite3
from sqlite3 import Error

URL_DB = r"C:/Users/tranq/Documents/Semeter1_2022_2023/Semeter1_2022_2023/Handle Image/Recognization_My_Friends/Buoc3/DB/sqlite.db"


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_db(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(conn, user):
    sql = ''' INSERT INTO users(name,age,image,description)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def main():
    database = URL_DB
    # Create table
    sql_create_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        age integer NOT NULL,
                                        image text  NOT NULL,
                                        description text NOT NULL
                                    ); """
    # Delete table
    sql_delete_table = """ DROP TABLE users """

    conn = create_connection(database)

    if conn is not None:
        # create table when connection exist
        create_table(conn, sql_create_table)

    else:
        print("Error! cannot create the database connection.")


def insertUser(conn):
    user = ("Đức Hòa", 21, "BanNinh_0001",
            "Thích lập trình web")
    userId = create_user(conn, user)
    print(userId)


def select_all_users(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def get_user_by_name(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name = ?", (name,))

    rows = cur.fetchall()

    for row in rows:
        print(row)


if __name__ == '__main__':
    """Create file sqlite.db"""
    # create_db(r"C:/Users/tranq/Documents/Semeter1_2022_2023/Semeter1_2022_2023/Handle Image/Recognization_My_Friends/Buoc3/DB/sqlite.db")
    """Create table, deletable, read data"""
    # main()

    database = URL_DB
    conn = create_connection(database)
    with conn:
        """insert data"""
        # insertUser(conn)
        """Get all data"""
        get_user_by_name(conn, "Đức Hòa")