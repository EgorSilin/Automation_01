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
                    # f.write(fieldDesc[fdb.DESCRIPTION_NAME].ljust(fieldDesc[fdb.DESCRIPTION_DISPLAY_SIZE]) + '\n')  # , end="|"
                    f.write(fieldDesc[fdb.DESCRIPTION_NAME] + ';')  # , end="|"
                f.write('\n')
                # вывод данных таблицы
                field_indices = range(len(cur_fb_db.description))
                for row in cur_fb_db:
                    for fieldIndex in field_indices:
                        field_value = str(row[fieldIndex])
                        # fieldMaxWidth = cur_fb_db.description[fieldIndex][fdb.DESCRIPTION_DISPLAY_SIZE]
                        # f.write(fieldValue.ljust(fieldMaxWidth) + '|')  # , end="|"
                        f.write(field_value + ';')  # , end="|"
                    f.write('\n')
                cur_fb_db.close()
            finally:
                con_fb_db.close()
    except IOError:
        sys.exit("Data file(-s) already exist!")


def file_to_mysql():
    """Read text file to list of lists"""  # Оптимизировать на построчное чтение
    # MySQL #######################################################
    # Open database connection
    con_mysql_db = get_con_mysql_db()
    try:
        # prepare a cursor object using cursor() method
        cur_mysql_db = con_mysql_db.cursor()

        # execute SQL query using execute() method.
        try:
            # Execute the SQL command
            cur_mysql_db.execute("show tables")
            cur_mysql_db.execute("DELETE FROM FIRST_LAST_NAME;")
            fn_file = csv.reader(open('/home/user/first_name.csv'), delimiter=';')
            # sql = """INSERT INTO FIRST_LAST_NAME(id,first_name,last_name) VALUES(%d,%s,%s)"""
            sql = """INSERT INTO FIRST_LAST_NAME(id,first_name) VALUES(%i,%s,%s)"""
            next(fn_file)
            for line in fn_file:
                line = [None if cell == '' else cell for cell in line]
                print(line)
                print(int(line[0]), line[1], line[2])
                # cur_mysql_db.execute(sql, line)
                cur_mysql_db.execute(sql, [int(line[0]), line[1], line[2]])

            # cur.execute("SELECT * FROM cities WHERE id=%s", myid)

            con_mysql_db.commit()
        except:
            # Rollback in case there is any error
            print(f'Transaction Error')
            cur_mysql_db.rollback()

        # Fetch a single row using fetchone() method.
        data = cur_mysql_db.fetchall()
        print(data)

        cur_mysql_db.close()
    finally:
        # disconnect from server
        con_mysql_db.close()
    # MySQL END ###################################################################

    # ####################################################
    # lst_of_str = []
    # try:
    #     with open(path, 'r') as f:
    #         for line in f:
    #             lst_of_str.append([line.split(';')[0], line.split(';')[1]])
    #             # print(line)  # for TS
    # except IOError:
    #     print("Read data file error!")
    # print(lst_of_str)  # for TS
    # #####################################################


if __name__ == '__main__':
    # Чтение в файл из firebird
    fb_to_file(path='/home/user/first_name.csv',
               sql_req="SELECT id, first_name FROM FIRST_NAME")
    fb_to_file(path='/home/user/last_name.csv',
               sql_req="SELECT id, last_name FROM LAST_NAME")
    # if os.path.exists('/home/user/first_name.txt') and os.path.exists('/home/user/first_name.txt'):
    #     sys.exit("Data file(-s) already exist!")
    # else:
    #     write_to_file(path='/home/user/first_name.txt',
    #                   sql_req="SELECT ID,NAME FROM FIRST_NAME")
    #     write_to_file(path='/home/user/last_name.txt',
    #                   sql_req="SELECT ID,NAME FROM LAST_NAME")

    # Чтение из файла
    # data_files_path = 'C:\Users\EgorS\PycharmProjects\Automation_01\data_files'
    # file_to_mysql(path='/home/user/first_name.csv')
    # file_to_mysql(path='/home/user/last_name.csv')
    file_to_mysql()


