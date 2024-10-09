import pymysql

# connect with mysql
conn = pymysql.connect(host="localhost", port=3306, user="root",
                       password="Love=@201314", database="my_database",
                       cursorclass = pymysql.cursors.DictCursor)

with conn:
    with conn.cursor() as cursor:
        sql = "SELECT * FROM school_student_info WHERE class_name = %s;"
        cursor.execute(sql, ('三年级一班', ))
        # obtain all data
        #print(cursor.fetchall())

        # obtain only one data
        print(cursor.fetchone())
        print(cursor.fetchone())

        # obtain certain number of data
        data_list = cursor.fetchmany(10) # continues from above search
        for item in data_list:
            print(item['stu_name'])

        sql = "UPDATE school_student_info SET stu_name = '小李明' WHERE stu_no = 1001;"
        cursor.execute(sql) # need to commit this action

        stu_no = 1047
        stu_name = '王利明'
        sql = "INSERT INTO school_student_info(stu_no, stu_name) VALUES (%s, %s);"
        cursor.execute(sql, (stu_no, stu_name))

        # INSERT A BATCH OF DATA
        data = ((1048, '学生1'), (1049, '学生2'), (1050, '学生3'))
        cursor.executemany(sql, data)

        # Database Transaction - collection of operations on database
        # Rollback - return to the original state
        sql = "INSERT INTO school_student_info(stu_no, stu_name) VALUES (1052, '名字2')"
        sql1 = "INSERT INTO school_student_info(stu_no, stu_name) VALUES (1051, '名字1')"
        sql2=  "INSERT INTO school_course_info(course_name, teacher) VALUES ('地理')"

        try:
            cursor.execute(sql) # this will be success
            conn.begin()  # start transaction - if one failed, all failed
            cursor.execute(sql1) # these two will not proceed since sql2 failed
            cursor.execute(sql2)
            conn.commit()
        except Exception as e:
            conn.rollback()
            print('Rollback') # will roll back to the point where the transaction starts (line 40)

        name = "名字2"
        sql = "DELETE FROM school_student_info WHERE stu_name = %s"
        cursor.execute(sql, (name,))

    conn.commit()