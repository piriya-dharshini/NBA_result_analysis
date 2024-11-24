# CONNECTING TO THE DATABASE

import mysql.connector
mydb = mysql.connector.connect(
   host =  "localhost",
   user = "ur username",
   passoword = "ur password",
   database = "Result_Analysis"
)
cur = mydb.cursor()
import os

# NECESSARY IMPORTS OF FUCTIONS OR MODULES

from database import drop_tables, create_tables
# Clearing the table spaces and dropping the tables of the database
# drop_tables()
# Creating the tables
# create_tables()


# For reading the raw data from the excel file
from read_excel import *

def reading_excel(excel_file):
        data = read_sheet(excel_file)
        final_val = filter_data(data)
        return final_val

# USER DEFINED FUNCTIONS

def GPA(register_no, semester):

    '''
    For updating the GPA column with the GPA value for each student
    in the Student relation
    '''

    select = f'''SELECT SUM(g.Point * c.credit), SUM(c.credit)
            FROM Grade_Point g, Result_data r, Credit_Info c
            WHERE r.Course_Code = c.Course_Code
            AND r.Grade = g. Grade
            AND r.Register_No = {register_no}
            AND r.semester = {semester}'''
    cur.execute(select)
    data = cur.fetchone()
    # print(data)
    if data !=(None,None):
        return round(data[0] / data[1], 3)
    else:
        return 0

def CGPA(register_no):

    '''
    For updating the CGPA column with the GGPA value for each student
    in the Student relation
    '''

    select = f'''SELECT SUM(g.Point * c.credit), SUM(c.credit)
            FROM Grade_Point g, Result_data r, Credit_Info c
            WHERE r.Course_Code = c.Course_Code
            AND r.Grade = g. Grade
            AND r.Register_No = {register_no}
            '''
    cur.execute(select)
    data = cur.fetchone()
    # print(data)
    if data !=(None,None):
        return round(data[0] / data[1], 3)
    else:
        return 0

def Backlogs(register_no, semester):
    '''
    For updating the backlogs and history of arrears column
    in the Student relation
    '''

    select = f'''SELECT r.Grade
            FROM Result_data r
            WHERE r.Register_No = {register_no} and Semester={semester}'''
    
    upgrade = f'''SELECT g.history_of_arrears
        FROM grades g
        WHERE g.Register_No={register_no}
    '''
    cur.execute(select)
    data = cur.fetchall()
    cur.execute(upgrade)

    hoa = cur.fetchall()
    count = 0 # Number of Backlogs
    history_of_arrears = '0' 
    # Boolean Value - Made True in case of arrear in any subject
    if hoa == []:
        # print('in0')
        for item in data:
            if item[0] == 'RA' or item[0] == 'U':
                count += 1
                history_of_arrears = '1'

    elif hoa == [('1',)]:
        # print('in1')
        for item in data:
            if item[0] == 'RA' or item[0]=='U':
                count += 1
        history_of_arrears = '1'

    elif hoa == [('0',)]:
        # print('in2')
        for item in data:
            if item[0] == 'RA' or item[0]=='U':
                count += 1
                history_of_arrears = '1'

    # print('REGISTERNO:',register_no)
    # print(data)
    # print(hoa)
    # print('After:',history_of_arrears)
    # print('---------------------------')
    return count, history_of_arrears


def GradePoint():

    '''
    For inserting the Grade and corresponding
    point in the Grade_Point relation
    '''

    # TABLE
    # Grade_Point
    #    Grade CHAR(2) PRIMARY KEY,
    #    Point INT

    data = [('O', 10), ('A+', 9), ('A', 8), ('B+', 7), ('B', 6), ('C', 5), ('RA', 0), ('U', 0), ('AB', 0), ('WH', 0),('SA',0)]

    insert = '''INSERT INTO Grade_Point(Grade, Point)
        VALUES (%s, %s)'''
    cur.executemany(insert, data)
    mydb.commit()


def CreditInfo():

    '''
    For inserting the Course Code, Course Title
    and Credit of all the courses
    in the Credit_Info relation
    '''

    # TABLE
    # Credit_Info
    #     Semester INT,
    #     Course_Code CHAR(7) PRIMARY KEY,
    #     Course_Title Char(70) UNIQUE,
    #     Credit FLOAT

    data = [
    (1, 'UCY2176', 'Engineering Chemistry', 3, 2021),
    (1, 'UEN2176', 'Technical English', 3, 2021),
    (1, 'UGE2176', 'Problem Solving and Programming in Python', 3, 2021),
    (1, 'UGE2177', 'Engineering Graphics', 3, 2021),
    (1, 'UGE2197', 'Programming in Python Laboratory', 1.5, 2021),
    (1, 'UGS2197', 'Physics and Chemistry Laboratory', 1.5, 2021),
    (1, 'UMA2176', 'Matrices and Calculus', 4, 2021),
    (1, 'UPH2176', 'Engineering Physics', 3, 2021),
    (2, 'UMA2276', 'Complex Functions and Laplace Transforms', 4, 2021),
    (2, 'UEE2276', 'Basic Electrical and Electronics Engineering', 3, 2021),
    (2, 'UIT2201', 'Programming and Data Structures', 4, 2021),
    (2, 'ACY2276', 'Environmental Science', 0, 2021),
    (2, 'UPH2251', 'Physics for Information Science and Technology', 3, 2021),
    (2, 'UGA2176', 'Heritage of Tamils', 1, 2021),
    (2, 'UIT2211', 'Software Development Project I', 1.5, 2021),
    (2, 'UGE2297', 'Design Thinking and Engineering Practices Lab', 1.5, 2021),
    (2, 'UEN2241', 'Language and communications', 3, 2021),
    (2, 'UHS2241', 'Human relations at work', 3, 2021),
    (2, 'UHS2242', 'Applications of psychology in everyday life', 3, 2021),
    (2, 'UHS2243', 'Film Appreciation', 3, 2021),
    (3, 'UGA2276', 'Tamils and Technology', 1, 2021),
    (3, 'UHS2376', 'Universal Human Values 2 : Understanding Harmony', 3, 2021),
    (3, 'UIT2301', 'Programming and Design Patterns', 3, 2021),
    (3, 'UIT2302', 'Database Technology', 3, 2021),
    (3, 'UIT2304', 'Digital Logic and Computer Organization', 3, 2021),
    (3, 'UIT2305', 'Introduction to Digital Communication', 3, 2021),
    (3, 'UIT2311', 'Database Technology Laboratory', 1.5, 2021),
    (3, 'UIT2312', 'Programming and Design Patterns Laboratory', 1.5, 2021),
    (3, 'UMA2377', 'Discrete Mathematics', 4, 2021),
    (4,'UIT2401','Microprocessor and Microcontroller',3, 2021),
    (4,'UIT2402','Advanced Data Structures and Algorithm Analysis',5, 2021),
    (4,'UIT2403','Data Communication and Networks',3, 2021),
    (4,'UIT2404','Automata Theory and Compiler Design',3, 2021),
    (4,'UIT2411','Network Programming Lab',1.5, 2021),
    (4,'UIT2412','Digital Systems and Microprocessor Lab',1.5, 2021),
    (4,'UMA2476','Probability and Statistics',4, 2021),
    (5,'UBA2541','Principles of Management',3, 2021),
    (5,'UIT2501','Principles of Software Engineering and Practices',3, 2021),
    (5,'UIT2502','Data Analytics and Visualization',4, 2021),
    (5,'UIT2503','Principles of Operating Systems',3, 2021),
    (5,'UIT2504','Artificial Intelligence',3, 2021),
    (5,'UIT2511','Software Development Project – II',1.5, 2021),
    (5,'UIT2512','Operating Systems Practices Lab',1.5, 2021),
    (5,'UIT2521','Information Theory and Applications',3, 2021),
    (5,'UIT2522','Optimization Techniques for Machine Learning',3, 2021),
    (5,'UIT2526','Software Architecture and Principles',3, 2021),
    (5,'UIT2622','Advanced Artificial Intelligence Techniques',3, 2021),

    (1, 'UEN1176', 'Communicative English', 3, 2018),
    (1, 'UMA1176', 'Algebra and Calculus', 4, 2018),
    (1, 'UPH1176', 'Engineering Physics', 3, 2018),
    (1, 'UCY1176', 'Engineering Chemistry', 3, 2018),
    (1, 'UGE1176', 'Problem Solving and Programming in Python', 3, 2018),
    (1, 'UGE1177', 'Engineering Graphics', 3, 2018),
    (1, 'UGE1197', 'Programming in Python Lab', 1.5, 2018),
    (1, 'UGS1197', 'Physics and Chemistry Lab', 1.5, 2018),

    (2, 'UEN1276', 'Technical English', 3, 2018),
    (2, 'UMA1276', 'Complex Functions and Laplace Transforms', 4, 2018),
    (2, 'UPH1276', 'Physics for Information Science', 3, 2018),
    (2, 'UCY1276', 'Environmental Science', 3, 2018),
    (2, 'UEE1276', 'Basic Electrical, Electronics and Measurement Engineering', 3.5, 2018),
    (2, 'UIT1201', 'Fundamentals of C Programming', 3.5, 2018),
    (2, 'UGE1297', 'Design Thinking and Engineering Practices Lab', 1.5, 2018),
    (2, 'UIT1211', 'C Programming Lab', 1.5, 2018),

    (3, 'UMA1377', 'Discrete Mathematics', 4, 2018),
    (3, 'UIT1301', 'Digital Electronics', 4, 2018),
    (3, 'UIT1302', 'Fundamentals of Data Structures', 3, 2018),
    (3, 'UIT1303', 'Principles of Analog and Digital Communication', 3, 2018),
    (3, 'UIT1304', 'Database Management Systems and Applications', 3, 2018),
    (3, 'UIT1305', 'Computer Organization', 3, 2018),
    (3, 'UIT1311', 'Programming and Data Structures Lab - I', 2, 2018),
    (3, 'UIT1312', 'Database Management Systems and Applications Lab', 2, 2018),

    (4, 'UMA1478', 'Probability and Statistics', 4, 2018),
    (4, 'UIT1401', 'Principles of Software Engineering', 3, 2018),
    (4, 'UIT1402', 'Information Theory and Applications', 3, 2018),
    (4, 'UIT1403', 'Microprocessors and Microcontrollers', 3, 2018),
    (4, 'UIT1404', 'Advanced Data Structures', 3, 2018),
    (4, 'UIT1405', 'Algorithm Design and Analysis', 3, 2018),
    (4, 'UIT1411', 'Microprocessor and Microcontroller Lab', 2, 2018),
    (4, 'UIT1412', 'Programming and Data Structures Lab - II', 2, 2018),

    (5, 'UIT1501', 'Finite Automata Theory', 3, 2018),
    (5, 'UIT1502', 'Principles of Operating Systems', 3, 2018),
    (5, 'UIT1503', 'Computer Networks and Its Applications', 4, 2018),
    (5, 'UIT1504', 'Introduction to Digital Signal Processing', 4, 2018),
    (5, 'UIT1505', 'Artificial Intelligence Concepts and Algorithms', 3, 2018),
    (5, 'UIT1511', 'Software Design Lab', 2, 2018),
    (5, 'UIT1512', 'Operating Systems Lab', 2, 2018),
    (5, 'UIT1521', 'Fundamentals of Digital Image Processing', 3, 2018),
    (5, 'UIT1522', 'Distributed Computing', 3, 2018),
    (5, 'UIT1523', 'Optimization Techniques', 3, 2018),
    (5, 'UIT1524', 'Computer Graphics and Multimedia', 3, 2018),

    (6, 'UIT1601', 'Principles of Compiler Design', 4, 2018),
    (6, 'UIT1602', 'Web Programming', 3, 2018),
    (6, 'UIT1603', 'Big Data Engineering', 3, 2018),
    (6, 'UIT1604', 'Machine Learning Fundamentals', 4, 2018),
    (6, 'UEN1497', 'Interpersonal Skills/Listening & Speaking', 1, 2018),
    (6, 'UIT1611', 'Web Programming Lab', 2, 2018),
    (6, 'UIT1623', 'Interactive System Design', 3, 2018),
    (6, 'UIT1624', 'Fundamentals of Reversible and Quantum Computing', 3, 2018),
    (6, 'UIT1625', 'Analysis and Design of Service Oriented Architecture', 3, 2018),
    (6, 'UCH1041', 'Renewable Energy Sources', 3, 2018),
    (6, 'UEC1041', 'Introduction to Internet Of Things', 3, 2018),
    (6, 'UEE1043', '', 3, 2018),
    (6, 'UME1041', 'Intellectual Property Rights', 3, 2018),
    (6, 'UME1043', 'Design thinking#', 3, 2018),

    (7, 'UIT1703', 'Management Principles and Practices', 3, 2018),
    (7, 'UIT1701', 'Cloud Computing and Virtualization', 3, 2018),
    (7, 'UIT1702', 'Network Security', 3, 2018),
    (7, 'UIT1711', 'Mobile Application Development Lab', 2, 2018),
    (7, 'UEN1597', 'Professional Communication Lab', 1, 2018),
    (7, 'UIT1721', 'Principles of Software Project Management', 3, 2018),
    (7, 'UIT1722', 'Agile Software Development', 3, 2018),
    (7, 'UIT1723', 'Developments and Operations (DevOps)', 3, 2018),
    (7, 'UIT1731', 'Introduction to Deep Learning', 3, 2018),
    (7, 'UCE1941', 'Air Pollution Management', 3, 2018),
    (7, 'UCH1943', 'Environmental Impact Assessment', 3, 2018),
    (7, 'UME1942', 'Innovation and Creativity', 3, 2018),
    (7, 'UME1943', 'Enterpreneurship', 3, 2018)
]

    insert = '''INSERT INTO Credit_Info(Semester, Course_Code, Course_Title, Credit,regulation) VALUES (%s, %s, %s, %s,%s)'''
    cur.executemany(insert, data)
    mydb.commit()


def ResultData(year, batch_year, semester, excel_file):

    '''
    For inserting the Register Number, Course Code,
    Grade and Cleared Year of all the students
    in the Result_Data relation
    '''

    # TABLE
    # Result_Data
    #   Register_No BIGINT,
    #   Course_Code CHAR(7),
    #   Grade CHAR(2),
    #   Cleared_Year CHAR(20),
    #   Batch_Year CHAR(9),
    #   Semester int,
    #   PRIMARY KEY(Register_No, Course_Code)

    column_name, column_values = reading_excel(excel_file)
    # print('COLUMN NAMES')
    # print(column_name)
    # print('COLUMN VALUES')
    # print(column_values)
    data = []
   
    # print(column_values)
    for new_index in range(2, len(column_name)):
        for index in range(len(column_values[0])):

            if column_values[new_index][index] == 'U' or column_values[new_index][index] == 'RA' or column_values[new_index][index] == 'AB' or column_values[new_index][index] == 'WH' or column_values[new_index][index] == 'SA':
                item = '-'
                data.append((column_values[0][index], column_name[new_index], column_values[new_index][index], item, batch_year,semester))

            elif column_values[new_index][index] == '-':
                item = 'NA'
                data.append((column_values[0][index], column_name[new_index], column_values[new_index][index], item, batch_year, semester))

            else:
                item = year
                data.append((column_values[0][index], column_name[new_index], column_values[new_index][index], item, batch_year, semester))
   
    insert = '''INSERT INTO Result_Data(Register_No, Course_Code, Grade, Cleared_Year, Batch_Year, semester) VALUES (%s, %s, %s, %s, %s, %s)'''
    cur.executemany(insert, data)
    mydb.commit()


def Student(batch_year, semester, excel_file):

    '''
    For inserting the Digital ID, Register Number, Name,
    Batch_Year, CGPA and Backlogs of all the students
    in the Student relation
    '''

    # TABLE
    # Student
    #   Digital_ID INT UNIQUE,
    #   Register_No BIGINT PRIMARY KEY,
    #   Name Char(40),
    #   Batch_Year CHAR(9),
    #   History_Of_Arrears VARCHAR(5)

    column_name, column_values = reading_excel(excel_file)

    data = [(column_values[0][index], column_values[1][index], batch_year) for index in range(len(column_values[0]))]   
    curr_stds=f'''SELECT * FROM Student where batch_year="{batch_year}"'''
    cur.execute(curr_stds)
    student=cur.fetchall()
    # print(data)
    if semester==1:
        insert = '''INSERT INTO Student(Register_No, Name, Batch_Year) VALUES ( %s, %s, %s)'''
        cur.executemany(insert, data)
        mydb.commit()
    if semester==3:
        print('batch year:',batch_year)
        ex_std=[]
        ct=0
        for i in data:
            reg=str(i[0])
            if int(reg[-3])==3:
                ex_std.append(i)
        insert = '''INSERT INTO Student(Register_No, Name, Batch_Year) VALUES ( %s, %s, %s)'''
        cur.executemany(insert, ex_std)
        mydb.commit()
    


def Grades(batch_year, semester, excel_file):

    '''
    For inserting the Digital ID, Register Number, Name,
    Batch_Year, CGPA and Backlogs of all the students
    in the Student relation
    '''

    # TABLE
    # Grades
    #   Register_No BIGINT,
    #   SEM1_GPA FLOAT,
    #   SEM2_GPA FLOAT,
    #   SEM3_GPA FLOAT,
    #   SEM4_GPA FLOAT,
    #   SEM5_GPA FLOAT,
    #   SEM6_GPA FLOAT,
    #   SEM7_GPA FLOAT,
    #   SEM8_GPA FLOAT,
    #   SEM1_HOA INT,
    #   SEM2_HOA INT,
    #   SEM3_HOA INT,
    #   SEM4_HOA INT,
    #   SEM5_HOA INT,
    #   SEM6_HOA INT,
    #   SEM7_HOA INT,
    #   SEM8_HOA INT,
    #   SEM1_CGPA FLOAT,
    #   SEM2_CGPA FLOAT,
    #   SEM3_CGPA FLOAT,
    #   SEM4_CGPA FLOAT,
    #   SEM5_CGPA FLOAT,
    #   SEM6_CGPA FLOAT,
    #   SEM7_CGPA FLOAT,
    #   SEM8_CGPA FLOAT,
    #   Currrent_Arrears INT,
    #   Batch_Year CHAR(9)
    column_name, column_values = reading_excel(excel_file)

    data = [(column_values[0][index], GPA(column_values[0][index],semester), Backlogs(column_values[0][index],semester)[0],CGPA(column_values[0][index]), Backlogs(column_values[0][index],semester)[1], batch_year) for index in range(len(column_values[0]))]
    # print(column_values[0])
    # print('backlogs')
    cur_data=f'''
            SELECT * FROM GRADES where batch_year="{batch_year}"'''
    cur.execute(cur_data)
    new_data=cur.fetchall()

    if semester == 1:
        insert = '''INSERT INTO Grades(Register_No, SEM1_GPA, SEM1_HOA,SEM1_CGPA, History_Of_Arrears, Batch_Year) VALUES (%s, %s, %s,%s, %s, %s)'''
        cur.executemany(insert, data)
        mydb.commit()

    elif semester == 2:
        for i in data: 
            update = f'''UPDATE Grades
                      SET SEM2_GPA = {i[1]},
                          SEM2_HOA = {i[2]},
                          SEM2_CGPA = {i[3]},
                          History_Of_Arrears = {i[4]}
                      WHERE Register_No = {i[0]}'''
            cur.execute(update)
            mydb.commit()

    elif semester == 3:
        for i in data: 
            update=f'''UPDATE Grades
                      SET SEM3_GPA = {i[1]},
                          SEM3_HOA = {i[2]},
                          SEM3_CGPA = {i[3]},
                          History_Of_Arrears = {i[4]}
                      WHERE Register_No={i[0]}'''
            cur.execute(update)
            mydb.commit()
        ex_std=[]
        ct=0
        for i in data:
            reg=str(i[0])
            if int(reg[-3])==3:
                ex_std.append(i)
            ct+=1
 
        update1 = '''INSERT INTO Grades(Register_No, SEM3_GPA, SEM3_HOA,SEM3_CGPA, History_Of_Arrears, Batch_Year) VALUES (%s, %s,%s, %s, %s, %s)'''
        cur.executemany(update1, ex_std)
        mydb.commit()
    else:
        val1 = 'SEM' + str(semester) + '_GPA'
        val2 = 'SEM' + str(semester) + '_HOA'
        val3 = 'SEM' + str(semester) + '_CGPA'
        for i in data: 
            update = f'''UPDATE Grades
                      SET {val1} = {i[1]},
                          {val2} = {i[2]},
                          {val3} = {i[3]},
                          History_Of_Arrears = {i[4]}
                      WHERE Register_No = {i[0]}'''
            cur.execute(update)
            mydb.commit()

def upgrade(year, batch_year, semester, excel_file):
    column_name, column_values = reading_excel(excel_file)
    # print('COLUMN VALUES')
    excel_data = []
    # print(column_name,column_values)
    for new_index in range(2, len(column_name)):
        for index in range(len(column_values[0])):
            if column_values[new_index][index] == 'U' or column_values[new_index][index] == 'RA' or column_values[new_index][index] == 'AB' or column_values[new_index][index] == 'WH' or column_values[new_index][index] == 'SA':
                item = '-'
                excel_data.append((column_values[0][index], column_name[new_index], column_values[new_index][index], item, batch_year,semester))

            elif column_values[new_index][index] == '-':
                item = 'NA'
                excel_data.append((column_values[0][index], column_name[new_index], column_values[new_index][index], item, batch_year,semester))

            else:
                item = year
                excel_data.append((column_values[0][index], column_name[new_index], column_values[new_index][index], item, batch_year,semester))

    for i in excel_data:
        # print(i)
        upgrade = f'''
                UPDATE result_data
                set grade = '{i[2]}'
                where batch_year = '{batch_year}' 
                and semester = {semester} 
                and register_no = {i[0]} 
                and Course_code = '{i[1]}'
                '''
        cur.execute(upgrade)
        mydb.commit()

    grades_data = [(column_values[0][index], GPA(column_values[0][index],semester), Backlogs(column_values[0][index],semester)[0],CGPA(column_values[0][index]) ,Backlogs(column_values[0][index],semester)[1], batch_year) for index in range(len(column_values[0]))]
    val1 = 'SEM' + str(semester) + '_GPA'
    val2 = 'SEM' + str(semester) + '_HOA'
    val3 = 'SEM' + str(semester) + '_CGPA'
    for i in grades_data: 
            update = f'''UPDATE Grades
                      SET {val1} = {i[1]},
                          {val2} = {i[2]},
                          {val3} = {i[3]},
                          History_Of_Arrears = {i[4]}
                      WHERE Register_No = {i[0]}'''
            cur.execute(update)
            mydb.commit()


class InvalidUsernameorPassword(Exception):
    '''User defined exception to tell the user if the
    entered username or password is wrong'''
    pass

class CheckYourPassword(Exception):
    pass


def insert_into_login(login_id, uname, pword, status):
    '''This function is used to insert a new tuple of data into
    the Login table.'''

    cur.execute("INSERT INTO Login (Login_ID, Username, Password, status) VALUES (%s, %s, %s, %s)",
                (login_id, uname, pword, status))
    mydb.commit()

def insert_into_faculty(name, login_id):
    '''This function is used to insert a new tuple of data into
    the Faculty table.'''

    cur.execute("INSERT INTO Faculty (Faculty_Name, Login_ID) VALUES (%s, %s)",
                (name, login_id))
    mydb.commit()

def insert_into_faculty_batch(name, batch_year,status):
    '''This function is used to insert a new tuple of data into
    the Faculty table.'''

    cur.execute("INSERT INTO Faculty_batch(Faculty_Name,Batch_Year,status) VALUES (%s, %s,%s)",
                (name,batch_year,status))
    mydb.commit()


def login1(uname, pword):
    '''This function is used to verify the username and password
    entered with those in the database.
    If not valid, error is raised, else it is valid.'''

    sql_uname = "SELECT Username FROM Login"
    cur.execute(sql_uname)
    result_uname = cur.fetchall()

    try:
        if (uname,) in result_uname:

            sql_pword = "SELECT Password FROM Login WHERE Username = %s"
            cur.execute(sql_pword, (uname,))
            result_pword = cur.fetchone()

            if (pword,) == result_pword:
                return True
            else:
                raise InvalidUsernameorPassword("Please enter a valid Username or Password!!")

        else:
            raise InvalidUsernameorPassword("Please enter a valid Username or Password!!")

    except InvalidUsernameorPassword as e:
        print("Invalid Username or Password: ",e)


# # Calling the functions to insert the
# # records into the relations
# GradePoint()
# CreditInfo()
# # ResultData()
# # Student()
# # Grades()
# # print('backlogs')
# # Backlogs(3122225002092)
# # upgrade()
# # # Displaying the records

# # select = '''SELECT * FROM Grade_Point'''
# # cur.execute(select)
# # data = cur.fetchall()
# # print(data)

# # select = '''SELECT * FROM Credit_Info'''
# # cur.execute(select)
# # data = cur.fetchall()
# # print(data)

# # select = '''SELECT * FROM Result_Data'''
# # cur.execute(select)
# # data = cur.fetchall()
# # print(data)

# # select = '''SELECT * FROM Student'''
# # cur.execute(select)
# # data = cur.fetchall()
# # print(data)

# # select = '''SELECT * FROM Grades'''
# # cur.execute(select)
# # data = cur.fetchall()
# # print(data)

# if __name__=='__main__':
#         login = [(13, 'gayathriks@ssn.edu.in', 'ssnstaff@12', 'Faculty'),
#                         (17, 'sofiajenniferj@ssn.edu.in', 'ssnstaff@16', 'Faculty'),
#                         (25, 'sornavallig@ssn.edu.in', 'ssnstaff@24', 'Faculty')]

#         for data in login:
#             insert_into_login(data[0], data[1], data[2], data[3])

#         faculty_table_data = [
#                             ('K. S. Gayathri', 13),
#                             ('J. Sofia Jennifer', 17),
#                             ('G. Sornavalli', 25),
#                         ]
#         for data in faculty_table_data:
#             print(data)
#             insert_into_faculty(data[0], data[1])

#         faculty_batch_status=[
#                             ('K. S. Gayathri', '2023-2027','permanent'),
#                             ('J. Sofia Jennifer', '2021-2025','permanent'),
#                             ('G. Sornavalli', '2023-2027','temporary'),
#                             ('G. Sornavalli', '2022-2026','permanent'),
#                             ('G. Sornavalli', '2021-2025','temporary'),
#                             ('G. Sornavalli', '2020-2024','temporary'),
                            
#                         ]

#         for data in faculty_batch_status:
#             print(data)
#             insert_into_faculty_batch(data[0], data[1],data[2])