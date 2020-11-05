import sys
import fdb
import pymysql


def get_con_fb_db():
    con_fb_db_int = fdb.connect(dsn='127.0.0.1:/var/lib/firebird/3.0/data/name_db.fdb',
                                user='sysdba',
                                password='user@7136498',
                                charset='UTF8')
    return con_fb_db_int


def get_con_mysql_db():
    con_mysql_db_int = pymysql.connect(host="localhost",
                                       user="root",
                                       password="root@mysql",
                                       db="name_db")
    return con_mysql_db_int


def write_to_file(path, sql_req):
    # Запись в файл
    try:
        with open(path, 'w') as f:  # W - for test; X - for prod;
            con_fb_db = get_con_fb_db()
            try:
                cur_fb_db = con_fb_db.cursor()
                cur_fb_db.execute(sql_req)
                ########
                for fieldDesc in cur_fb_db.description:
                    # f.write(fieldDesc[fdb.DESCRIPTION_NAME].ljust(fieldDesc[fdb.DESCRIPTION_DISPLAY_SIZE]) + '\n')  # , end="|"
                    f.write(fieldDesc[fdb.DESCRIPTION_NAME] + '|')  # , end="|"
                f.write('\n')
                # вывод данных таблицы
                fieldIndices = range(len(cur_fb_db.description))
                for row in cur_fb_db:
                    for fieldIndex in fieldIndices:
                        fieldValue = str(row[fieldIndex])
                        fieldMaxWidth = cur_fb_db.description[fieldIndex][fdb.DESCRIPTION_DISPLAY_SIZE]
                        # f.write(fieldValue.ljust(fieldMaxWidth) + '|')  # , end="|"
                        f.write(fieldValue + '|')  # , end="|"
                    f.write('\n')
                ########
                cur_fb_db.close()
            finally:
                con_fb_db.close()
    except IOError:
        sys.exit("Data file(-s) already exist!")


if __name__ == '__main__':
    write_to_file(path='/home/user/first_name.txt',
                  sql_req="SELECT ID,NAME FROM FIRST_NAME")
    write_to_file(path='/home/user/last_name.txt',
                  sql_req="SELECT ID,NAME FROM LAST_NAME")
    # data_files_path = 'C:\Users\EgorS\PycharmProjects\Automation_01\data_files'
    # Чтение из файла
    lst_of_str = []
    try:
        with open('/home/user/first_name.txt', 'r') as f:
            for line in f:
                lst_of_str.append([line.split('|')[0], line.split('|')[1]])
                print(line)
    except IOError:
        print("An IOError has occurred!")
    print(lst_of_str)

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
            # Commit your changes in the database
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
