# import mysql.connector, time

# my_sql = mysql.connector.connect(host='localhost', user='root', passwd=r'vishal@sql@123', database='Data_collector')

# my_cursor = my_sql.cursor()


# # my_cursor.execute("CREATE DATABASE users")

# # my_cursor.execute("SHOW TABLES")
# my_cursor.execute('DESC `sql result`;')
# r = my_cursor.fetchall()
# for i in r:
#     print(i[0])
# print(my_cursor.fetchall())

# my_cursor.execute("CREATE TABLE user_details(user_id INTEGER AUTO_INCREMENT primary key)")
# my_cursor.execute("ALTER TABLE user_details ALTER COLUMN user_id NOT NULL")
# my_cursor.execute("ALTER TABLE user_details ADD name VARCHAR(30);")
# def copy_from_sql_to_sqlite3():
import sqlite3
# mysqlite = sqlite3.connect('F:/vishal/codings/python files/PycharmProjects/Website/flask/flask_virtual/users.db')
mysqlite = sqlite3.connect('F:/vishal/codings/python files/PycharmProjects/Data_collector.db')

my_cursor = mysqlite.cursor()
# mycursor.execute("DROP table user_details")
# my_cursor.execute("PRAGMA table_info('users')")
my_cursor.execute('insert into table_123 values')
result = my_cursor.fetchall()

# sql_command = """create table user_details(login_id varchar(30) primary key, user_name varchar(30), password varchar(30) , dob char(10), age integer default 0 not null, qual varchar(30), occu varchar(30),
#             ph_no integer, filename varchar(150), data longblob);"""
# mycursor.execute(sql_command)
# for i in result:
#   data = i[9]
#   sql_command = "insert into user_details values('{}','{}','{}','{}',{} ,'{}', '{}', {}, '{}', %s);".format(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
#   mycursor.execute(sql_command, (data,))
#   mysqlite.commit()

# mycursor.execute("Select * from user_details")
# result = mycursor.fetchall()
for i in result:
    print(i)
# time.sleep(75)


# my_cursor.execute("DELETE user;")
# my_cursor.execute("DROP TABLE user_details")
# for i in range(1, 10):
# 	login_id = 'vishal@' + str(i)
# 	u_name = 'vishal' + str(i)
# 	dob = '15/01/20' + str(i)
# 	passwd = 'vishal@' + str(i)
# 	my_cursor.execute("INSERT INTO user_details VALUES ('{}', '{}', '{}', '{}', 'test', 'vetti', {});".format(login_id, u_name, passwd, dob, 123456789*10+i))
# 	my_sql.commit()
# #
# mycursor.execute("SELECT * FROM user_details")
# result = mycursor.fetchall()
# my_cursor.execute("select max(user_id) from user_details")
# user_id_val = my_cursor.fetchone()
# print(user_id_val[0])
# copy_from_sql_to_sqlite3()
# import sqlite3

# db_filename = 'database.sqlite'
# newline_indent = '\n   '

# db=sqlite3.connect('F:/vishal/codings/python files/PycharmProjects/Website/flask/flask_virtual/users.db')
# db.text_factory = str
# cur = db.cursor()

# result = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
# table_names = sorted(list(zip(*result))[0])
# print ("\ntables are:"+newline_indent+newline_indent.join(table_names))

# for table_name in table_names:
#     result = cur.execute("PRAGMA table_info('%s')" % table_name).fetchall()
#     column_names = list(zip(*result))[1]
#     print (("\ncolumn names for %s:" % table_name)
#            +newline_indent
#            +(newline_indent.join(column_names)))

# db.close()
# print ("\nexiting.")