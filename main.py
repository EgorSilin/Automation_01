import fdb
# import MySQLdb
import pymysql as my_sql_db

if __name__ == '__main__':
    con = fdb.connect(dsn='127.0.0.1:/var/lib/firebird/3.0/data/name_db.fdb',
                      user='sysdba',
                      password='user@7136498',
                      charset='UTF8')

    cur = con.cursor()
    cur.execute("select ID,NAME from FIRST_NAME")

    # Запись в файл
    try:
        with open('/home/user/first_name.txt', 'w') as f:
            for fieldDesc in cur.description:
                # f.write(fieldDesc[fdb.DESCRIPTION_NAME].ljust(fieldDesc[fdb.DESCRIPTION_DISPLAY_SIZE]) + '\n')  # , end="|"
                f.write(fieldDesc[fdb.DESCRIPTION_NAME] + '|')  # , end="|"
            f.write('\n')
            # f.write("=" * 45 + '\n')
            # вывод данных таблицы
            fieldIndices = range(len(cur.description))
            for row in cur:
                for fieldIndex in fieldIndices:
                    fieldValue = str(row[fieldIndex])
                    fieldMaxWidth = cur.description[fieldIndex][fdb.DESCRIPTION_DISPLAY_SIZE]
                    # f.write(fieldValue.ljust(fieldMaxWidth) + '|')  # , end="|"
                    f.write(fieldValue + '|')  # , end="|"
                f.write('\n')
    except IOError:
        print("An IOError has occurred!")

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

    cur.close()
    con.close()

    print(lst_of_str)

    ########################################################

    # ниже блок кода для работы с базой
    # создаем подключение к БД
    db = my_sql_db.connect(host="localhost", user="vash_user", passwd="vash_pass", db="py", charset='utf8')
    # используя метод cursor() получаем объект для работы с базой
    cursor = db.cursor()
    # формируем sql запрос на запись
    sql = """INSERT INTO zp(zp)
            VALUES ('%(zarplata)s')
            """ % {"zarplata": av_zp}
    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()

    # import pymysql as MySQLdb
    #
    # # Open database connection
    # db = MySQLdb.connect("localhost", "root", "root", "test")
    #
    # # prepare a cursor object using cursor() method
    # cursor = db.cursor()
    #
    # # execute SQL query using execute() method.
    # cursor.execute("show tables")
    #
    # # Fetch a single row using fetchone() method.
    # data = cursor.fetchall()
    # print(data)
    #
    # # disconnect from server
    # db.close()