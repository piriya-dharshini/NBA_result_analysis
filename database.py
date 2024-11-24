# CONNECTING TO THE DATABASE

import mysql.connector
mydb = mysql.connector.connect(
   host =  "localhost",
   user = "root",
   password = "pdk164@#",
   database = "Result_Analysis"
)
cur = mydb.cursor()


# USER DEFINED FUNCTIONS

def drop_tables():

   '''
   Clears the tablespace and drops all the tables
   in the database Result_Analysis
   '''

   cur.execute('USE Result_Analysis')

   alter1 = '''ALTER TABLE Faculty DISCARD TABLESPACE'''
   cur.execute(alter1)

   drop1 = '''DROP TABLE IF EXISTS Faculty'''
   cur.execute(drop1)

   mydb.commit()

   alter2 = '''ALTER TABLE Login DISCARD TABLESPACE'''
   cur.execute(alter2)

   drop2 = '''DROP TABLE IF EXISTS Login'''
   cur.execute(drop2)

   mydb.commit()

   alter3 = '''ALTER TABLE Result_Data DISCARD TABLESPACE'''
   cur.execute(alter3)

   drop3 = '''DROP TABLE IF EXISTS Result_Data'''
   cur.execute(drop3)

   mydb.commit()

   alter4 = '''ALTER TABLE Student DISCARD TABLESPACE'''
   cur.execute(alter4)

   drop4 = '''DROP TABLE IF EXISTS Student'''
   cur.execute(drop4)

   mydb.commit()

   alter5 = '''ALTER TABLE Grade_Point DISCARD TABLESPACE'''
   cur.execute(alter5)

   drop5 = '''DROP TABLE IF EXISTS Grade_Point'''
   cur.execute(drop5)

   mydb.commit()

   alter6 = '''ALTER TABLE Credit_Info DISCARD TABLESPACE'''
   cur.execute(alter6)

   drop6 = '''DROP TABLE IF EXISTS Credit_Info'''
   cur.execute(drop6)

   mydb.commit()

   alter7 = '''ALTER TABLE Grades DISCARD TABLESPACE'''
   cur.execute(alter7)

   drop7 = '''DROP TABLE IF EXISTS Grades'''
   cur.execute(drop7)

   mydb.commit()


def create_tables():

   '''
   Creates the tables in the database Result_Analysis
   '''

   cur.execute('USE Result_Analysis')

   sql1 = '''CREATE TABLE IF NOT EXISTS Login(
      Login_ID INT PRIMARY KEY AUTO_INCREMENT,
      Username CHAR(40) UNIQUE,
      Password VARCHAR(30),
      status ENUM('Faculty','Student','Admin')
   )'''

   cur.execute(sql1)


   sql2 = '''CREATE TABLE IF NOT EXISTS Student(
      Register_No BIGINT PRIMARY KEY,
      Name Char(40),
      Batch_Year CHAR(9)
   )'''

   cur.execute(sql2)


   sql3 = '''CREATE TABLE IF NOT EXISTS Credit_Info(
      Semester INT,
      Course_Code CHAR(7),
      Course_Title Char(70) ,
      Credit FLOAT,
      Regulation INT,
      PRIMARY KEY(Semester, Course_Code)
   )'''

   cur.execute(sql3)


   sql4 = '''CREATE TABLE IF NOT EXISTS Grade_Point(
      Grade CHAR(2) PRIMARY KEY,
      Point INT
   )'''

   cur.execute(sql4)


   sql5 = '''CREATE TABLE IF NOT EXISTS Result_Data(
      Register_No BIGINT,
      Course_Code CHAR(7),
      Grade CHAR(2),
      Cleared_Year CHAR(20),
      Batch_Year CHAR(9),
      semester int,
      PRIMARY KEY(Register_No, Course_Code)
   )'''

   cur.execute(sql5)


   sql6 = '''CREATE TABLE IF NOT EXISTS Faculty(
      Faculty_Name CHAR(40) PRIMARY KEY,
      Login_ID INT,
      FOREIGN KEY(Login_ID) REFERENCES Login(Login_ID)
   )'''

   cur.execute(sql6)

   sql7 = '''CREATE TABLE IF NOT EXISTS Grades(
      Register_No BIGINT,
      SEM1_GPA FLOAT,
      SEM2_GPA FLOAT,
      SEM3_GPA FLOAT,
      SEM4_GPA FLOAT,
      SEM5_GPA FLOAT,
      SEM6_GPA FLOAT,
      SEM7_GPA FLOAT,
      SEM8_GPA FLOAT,
      SEM1_HOA INT,
      SEM2_HOA INT,
      SEM3_HOA INT,
      SEM4_HOA INT,
      SEM5_HOA INT,
      SEM6_HOA INT,
      SEM7_HOA INT,
      SEM8_HOA INT,
      SEM1_CGPA FLOAT,
      SEM2_CGPA FLOAT,
      SEM3_CGPA FLOAT,
      SEM4_CGPA FLOAT,
      SEM5_CGPA FLOAT,
      SEM6_CGPA FLOAT,
      SEM7_CGPA FLOAT,
      SEM8_CGPA FLOAT,
      Currrent_Arrears INT,
      History_Of_Arrears VARCHAR(5),
      Batch_Year CHAR(9)
   )'''

   cur.execute(sql7)

   sql8='''CREATE TABLE IF NOT EXISTS faculty_batch(
            Faculty_Name CHAR(40),
            Batch_Year CHAR(10),
            status CHAR(40),
            FOREIGN KEY(Faculty_Name) REFERENCES Faculty(Faculty_Name),
            PRIMARY KEY(Faculty_Name,Batch_Year)

         )
         '''
   
   cur.execute(sql8)

