# CONNECTING TO THE DATABASE

import mysql.connector
mydb = mysql.connector.connect(
   host =  "localhost",
   user = "root",
   password = "pdk164@#",
   database = "Result_Analysis"
)
cur = mydb.cursor()


# NECESSARY IMPORTS OF FUCTIONS OR MODULES

# For reading the raw data from the excel file
from read_excel import filter_data

# column_name, column_values = filter_data()

import pandas as pd


# USER DEFINED FUNCTIONS

def Deviation(register_no, sem,batch_year):

    '''
    Returns the deviation from the average GPA
    for a student given the register number
    '''
    mydb.commit()

    select = f'''SELECT s.Register_No, g.{'SEM' + str(sem)}_GPA
            FROM Student s, Grades g
            WHERE s.Register_No = g.Register_No
            and g.batch_year="{batch_year}"
            '''
    cur.execute(select)
    reg_cgpa = cur.fetchall()
    
    average_GPA = 0 # Average GPA

    # Calculation of average GPA
    for item in reg_cgpa:
        if item[1] != None:
            average_GPA += item[1]
    average_GPA = round((average_GPA / len(reg_cgpa)), 3)

    select = f'''SELECT g.{'SEM' + str(sem)}_GPA FROM Grades g where g.Register_No = {register_no}'''
    cur.execute(select)
    data = cur.fetchone()[0]
    
    return round((data - average_GPA), 3)

# print(Deviation(205002123, 1))


def Grade_Count(grade, course_code,sem,batch_year):

    '''
    Returns the grade count of the given grade
    and for the given course
    '''
    try:
        select = f'''SELECT COUNT(r.Grade) FROM Result_Data r
                WHERE r.Course_Code = "{course_code}"
                and r.batch_year="{batch_year}"
                and r.semester={sem}
                GROUP BY r.Grade
                HAVING r.Grade = "{grade}"'''
        cur.execute(select)
        result = cur.fetchone()[0]
    except TypeError:
        result = 0

    return result

#print(Grade_Count('O', 'UIT2201',2,'2022-2026'))

def Total_Grades(course_code, semester,batch_year):
    """
    Returns the total number of students who received a grade for the given course in the specified semester.

    Args:
        course_code (str): The course code.
        semester (int): The semester number.

    Returns:
        int: The total number of students with grades.
    """
    return Registered(course_code,semester,batch_year) - Reappear(course_code, semester,batch_year) -Grade_Count('WH',course_code,semester,batch_year)-Grade_Count('AB',course_code,semester,batch_year)

def Registered(course_code,semester,batch_year):

    '''
    Returns the number of students appeared
    for the given course
    '''
    grade = '-'
    select = f'''SELECT COUNT(r.Grade) FROM Result_Data r
            WHERE r.Course_Code = "{course_code}"
            and r.batch_year="{batch_year}"
            AND r.semester={semester}
            AND r.Grade <> "{grade}"'''
    cur.execute(select)
    result = cur.fetchone()[0]

    return result

#print(Registered('UIT2201',2,'2022-2026'))


def Passed(course_code,sem,batch_year):

    '''
    Returns the number of students passed
    for the given course
    '''

    return Registered(course_code,sem,batch_year) - (Grade_Count('U', course_code,sem,batch_year)+Grade_Count('RA', course_code,sem,batch_year))

# print(Passed('UIT1523','2020-2024'))

def Reappear(course_code,sem,batch_year):
    """
    Returns the number of students who need to reappear for the given course in the specified semester.

    Args:
        course_code (str): The course code.
        semester (int): The semester number.

    Returns:
        int: The number of students reappearing.
    """

    return Grade_Count('U', course_code,sem,batch_year) + Grade_Count('RA', course_code,sem,batch_year)

def Pass_Percentage(course_code,sem,batch_year):

    '''
    Returns the pass percentage
    for the given course
    '''
    if Registered(course_code,sem,batch_year) == 0:
        return 0
    return round(((Registered(course_code,sem,batch_year) - (Grade_Count('U', course_code,sem,batch_year)+Grade_Count('RA', course_code,sem,batch_year))) / Registered(course_code,sem,batch_year)) * 100, 2)

# print(Pass_Percentage('UIT1523','2020-2024'))


def Grade_Point_Average(course_code,batch_year):

    '''
    Returns the grade point average
    for the given course
    '''

    # Dictionary with grade as key and correspoing point as value
    select = '''SELECT * FROM Grade_Point'''
    cur.execute(select)
    cp = cur.fetchall()
    credit_point = {cp[index][0] : cp[index][1] for index in range(len(cp))}

    grade = '-'
    select = f'''SELECT r.Grade FROM Result_Data r
            WHERE r.Course_Code = "{course_code}"
            and r.batch_year="{batch_year}"
            AND r.Grade <> "{grade}"'''
    cur.execute(select)
    result = cur.fetchall()
    result = [item[0] for item in result]

    grade_point_average = sum([credit_point[grade] for grade in result if grade != '-'])

    if Registered(course_code,batch_year) == 0:
        return 0
    return round(grade_point_average / Registered(course_code,batch_year), 2)

# print(Grade_Point_Average('UIT1523','2020-2024'))


def Rank(register_no, sem,batch_year):

    mydb.commit()

    select = f'''SELECT g.{'SEM' + str(sem)}_GPA FROM Grades g where g.batch_year="{batch_year}"'''
    cur.execute(select)
    cgpa = cur.fetchall()
    cgpa = [list(item) for item in cgpa if item[0] is not None]

    df = pd.DataFrame({'CGPA' : cgpa})
    df['Rank'] = df['CGPA'].rank(ascending = False)

    rank = []
    for item in list(df):
        rank.append(df[item].tolist())

    # Dictionary with gpa of the student as key and rank as value
    dict_rank = {rank[0][index][0] : int(rank[1][index]) for index in range(len(rank[0]))}

    select = f'''SELECT g.{'SEM' + str(sem)}_GPA FROM Grades g WHERE g.Register_No = {register_no}'''
    cur.execute(select)
    student_cgpa = cur.fetchone()[0]

    return dict_rank[student_cgpa]


def Grade_Analysis(register_no, sem = 1):

    '''
    To analyze the count of each grade secured 
    by all students in a particular sem.
    '''

    dic = {}

    select_queries = [
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'O'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'A+'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'A'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'B+'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'B'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'C'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'RA'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'U'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'AB'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'WH'""",
            """SELECT count(*) FROM result_data r WHERE 
            r.Register_No = %s AND r.semester = %s AND r.grade = 'SA'"""
        ]

    for idx, query in enumerate(select_queries, start=1):

        cur.execute(query, (register_no, sem))
        count = cur.fetchone()[0]
        grade = ['O', 'A+', 'A', 'B+', 'B', 'C', 'RA', 'U', 'AB', 'WH', 'SA'][idx - 1]
        dic[grade] = count
    dic['RA'] = dic['RA'] + dic['U']

    return dic


def Grade_Count_Student(register_no, sem, grade):

    dic = Grade_Analysis(register_no, sem)

    return dic[grade]


def semester_data(semester,batch_year):
    """
    Fetches semester data from the database and returns a list of unique course codes.

    Args:
        semester (int): The semester number.

    Returns:
        list: A list of unique course codes for the specified semester.
    """
    s=f'''SELECT DISTINCT course_code FROM result_data WHERE semester={semester}
        and batch_year="{batch_year}"'''
    cur.execute(s)
    res=cur.fetchall()
    res=[data[0] for data in res]
    #print(res)

    return res 
#semester_data(2,'2022-2026')

def tot_candid(sem,batch_year):
    '''This functions returns the headcount of
    the total number of students who registered
    for the exam.
    '''
    grade='-'
    select = f'''SELECT COUNT(distinct(r.Register_No)) 
            FROM Result_Data r
            WHERE r.semester = "{sem}"
            AND r.batch_year="{batch_year}"
            AND r.Grade <> "{grade}"'''
    
    cur.execute(select)
    result = cur.fetchone()[0]  # Fetch the count from the result
    return result

def Appeared(course_code, semester,batch_year):
    """
    Returns the number of students who appeared for the given course in the specified semester.

    Args:
        course_code (str): The course code.
        semester (int): The semester number.

    Returns:
        int: The number of students appeared.
    """
    s=f'''SELECT COUNT(distinct(rd.Register_No))
            FROM result_data rd
            WHERE rd.course_code = "{course_code}"
                AND rd.semester = "{semester}"
                AND rd.batch_year="{batch_year}"
                AND rd.grade <>"{'AB'}"
                AND rd.grade <>"{'-'}" '''
    cur.execute(s)
    res=cur.fetchone()[0]
    #print(res)
    return res
