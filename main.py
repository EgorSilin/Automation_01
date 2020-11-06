import csv
import os
import sys
import fdb
import pymysql


def get_con_fb_db():
    """Connect to firebird"""
    con_fb_db_int = fdb.connect(dsn='127.0.0.1:/var/lib/firebird/3.0/data/name_db.fdb',
                                user='sysdba',
                                password='user@7136498',
                                charset='UTF8')
    return con_fb_db_int


def get_con_mysql_db():
    """Connect to mysql"""
    con_mysql_db_int = pymysql.connect(host="localhost",
                                       user="root",
                                       password="root@mysql",
                                       db="name_db")
    return con_mysql_db_int


def fb_to_file(path, sql_req):
    """Take data from firebird table and put in file"""
    try:
        with open(path, 'w') as f:  # W - for test; X - for prod;
            con_fb_db = get_con_fb_db()
            try:
                cur_fb_db = con_fb_db.cursor()
                cur_fb_db.execute(sql_req)
                for fieldDesc in cur_fb_db.description:
                    # f.write(fieldDesc[fdb.DESCRIPTION_NAME] + ';')
                    if fieldDesc != cur_fb_db.description[-1]:
                        f.write(fieldDesc[fdb.DESCRIPTION_NAME] + ';')
                    else:
                        f.write(fieldDesc[fdb.DESCRIPTION_NAME])
                f.write('\n')
                # Insert data in CSV
                field_indices = range(len(cur_fb_db.description))
                for row in cur_fb_db:
                    for fieldIndex in field_indices:
                        field_value = str(row[fieldIndex])
                        # f.write(field_value + ';')
                        if fieldIndex != field_indices[-1]:
                            f.write(field_value + ';')
                        else:
                            f.write(field_value)
                    f.write('\n')
                cur_fb_db.close()
            finally:
                con_fb_db.close()
    except IOError as e:
        sys.exit(f"Data file(-s) already exist! Error: {e}")
    else:
        print(f'Transfer from Firebird to CVS: - SUCCESS!')


def file_to_mysql(path_int):
    """Read text file to list of lists"""
    # Open database connection
    con_mysql_db = get_con_mysql_db()
    try:
        # prepare a cursor object using cursor() method
        cur_mysql_db = con_mysql_db.cursor()

        # execute SQL query using execute() method.
        try:
            # Execute the SQL command
            with open(f'{path_int}first_name.csv') as csv_file:
                cur_mysql_db.execute("DELETE FROM FIRST_LAST_NAME;")
                fn_file = csv.reader(csv_file, delimiter=';')
                # sql = """INSERT INTO FIRST_LAST_NAME(id,first_name,last_name) VALUES(%s,%s,%s)"""
                sql = """INSERT INTO FIRST_LAST_NAME(id,first_name) VALUES(%s,%s)"""
                next(fn_file)
                for line in fn_file:
                    line = [None if cell == '' else cell for cell in line]
                    cur_mysql_db.execute(sql, line[0:2])

            with open(f'{path_int}last_name.csv') as csv_file:
                fn_file = csv.reader(csv_file, delimiter=';')
                # sql = """INSERT INTO FIRST_LAST_NAME(id,first_name,last_name) VALUES(%s,%s,%s)"""
                sql = """UPDATE FIRST_LAST_NAME SET last_name = %s WHERE id = %s"""
                next(fn_file)
                for line in fn_file:
                    line = [None if cell == '' else cell for cell in line]
                    cur_mysql_db.execute(sql, line[1::-1])
            con_mysql_db.commit()
        except Exception as e:
            # Rollback in case there is any error
            print(f'Transaction Error: {e}')
            cur_mysql_db.rollback()
        cur_mysql_db.close()
    except Exception as e:
        print({e})
    else:
        print('Transfer from CVS to Mysql - SUCCESS!')
    finally:
        # disconnect from server
        con_mysql_db.close()


if __name__ == '__main__':
    path_to_csv = '/home/user/'
    if (os.path.exists(f'{path_to_csv}first_name.txt') or os.path.exists(f'{path_to_csv}last_name.txt')) is True:
        # True - for test; False - for prod;
        sys.exit("Data file(-s) already exist!")
    else:
        fb_to_file(path=f'{path_to_csv}first_name.csv',
                   sql_req="SELECT id, first_name FROM FIRST_NAME")
        fb_to_file(path=f'{path_to_csv}last_name.csv',
                   sql_req="SELECT id, last_name FROM LAST_NAME")
        file_to_mysql(path_to_csv)
        print('Script job - SUCCESS!')


