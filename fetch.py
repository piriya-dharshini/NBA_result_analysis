from insert_values import *
import os
import mysql.connector
from download_excel import write_to_excel
from analysis import *
from summary import *

# CONNECTING TO THE DATABASE

import mysql.connector
mydb = mysql.connector.connect(
   host =  "localhost",
   user = "ra",
   password = "1234",
   database = "Result_Analysis"
)

cur  =  mydb.cursor(buffered  =  True)

from analysis import Deviation, Rank, Grade_Count_Student

def statistics_data(register_no, semester,batch_year):

    select  =  f'''SELECT SUM(g.Point * c.credit)
            FROM Grade_Point g, Result_data r, Credit_Info c
            WHERE r.Course_Code  =  c.Course_Code
            AND r.Grade  =  g. Grade
            AND r.Register_No  =  {register_no}
            AND r.semester  =  {semester}
            and r.batch_year="{batch_year}"'''
    cur.execute(select)
    data  =  cur.fetchone()[0]

    select  =  f'''SELECT r.Register_No, s.Name,
            {Grade_Count_Student(register_no, semester, 'O')},
            {Grade_Count_Student(register_no, semester, 'A+')},
            {Grade_Count_Student(register_no, semester, 'A')},
            {Grade_Count_Student(register_no, semester, 'B+')},
            {Grade_Count_Student(register_no, semester, 'B')},
            {Grade_Count_Student(register_no, semester, 'C')},
            {Grade_Count_Student(register_no, semester, 'RA')},
            {Grade_Count_Student(register_no, semester, 'AB')},
            {Grade_Count_Student(register_no, semester, 'WH')},
            {Grade_Count_Student(register_no, semester, 'SA')},
            {data}, g.{'SEM'  +  str(semester)}_GPA, g.{'SEM'  +  str(semester)}_CGPA, {Deviation(register_no, semester,batch_year)},
            g.{'SEM'  +  str(semester)}_HOA, {Rank(register_no, semester, batch_year)}
            FROM Grades g, Result_data r, Student s
            WHERE r.Register_No  =  s.Register_No
            AND g.Register_No  =  r.Register_No
            AND r.Register_No  =  {register_no}
            and r.batch_year="{batch_year}"
                '''
    cur.execute(select)
    data = cur.fetchone()
    
    return list(data)


def display_statistics(semester,batch_year):

    data = []
    count = 1
    select = f'''SELECT DISTINCT(r.Register_No)
            FROM Result_data r, Student s
            WHERE r.Register_No = s.Register_No
            AND r.semester = {semester}
            and r.batch_year="{batch_year}"
            '''
    cur.execute(select)
    reg_no = cur.fetchall()
    reg_no = [item[0] for item in reg_no]

    for item in reg_no:
        row = statistics_data(item, semester,batch_year)
        row[11] = round(float(row[11]), 1)
        row[12] = round(float(row[12]), 3)
        row[13] = round(float(row[13]), 3)
        row[14] = round(float(row[14]), 3)
        row[11] = int(row[11])
        row[16] = 'FAIL' if (row[16] != 0 or row[9] != 0 or row[10] != 0 or row[11] != 0) else 'PASS'
        row.insert(0, count)
        data.append(row)
        count += 1

    return data

# print(display_statistics(3,'2020-2024'))


def uploadpost(batchyear, status, excel_file, semester):

        semester =  int(semester)
        year =  int(batchyear[:4])
        if status  ==  'beforeReval':
            if semester  ==  1:
                year = 'November' + ' ' + str(int(batchyear[:4]))
            elif semester  ==  2:
                year = 'May' + ' ' + str(int(batchyear[:4]) + 1)
            elif semester  ==  3:
                year = 'November' + ' ' + str(int(batchyear[:4]) + 1)
            elif semester  ==  4:
                year = 'May' + ' ' + str(int(batchyear[:4]) + 2)
            elif semester  ==  5:
                year = 'November' + ' ' + str(int(batchyear[:4]) + 2)
            elif semester  ==  6:
                year = 'May' + ' ' + str(int(batchyear[:4]) + 3)
            elif semester  ==  7:
                year = 'November' + ' ' + str(int(batchyear[:4]) + 3)
            else:
                year = 'May' + ' ' + str(int(batchyear[:4]) + 4)

            ResultData(year, batchyear,semester,excel_file)
            Student(batchyear,semester,excel_file)
            Grades(batchyear,semester,excel_file)
            # print('successfully completed')
            mydb.commit()
        elif status  ==  'afterReval':
            upgrade(year,batchyear,semester,excel_file)

        mydb.commit()


def getresultdata(user_id):

            sql1  =  "SELECT login_id FROM login WHERE username  =  %s"
            cur.execute(sql1, (user_id,))
            login_id  =  cur.fetchone()


            sql2 = "SELECT faculty_name from faculty where login_id = %s"
            cur.execute(sql2, login_id)

            faculty_name = cur.fetchone()
            # print('batch year', batch_year)
            # print(faculty_name)
            sql3="SELECT DISTINCT batch_year FROM faculty_batch WHERE faculty_name = %s"
            cur.execute(sql3,faculty_name)
            batch_years=cur.fetchall()
            # print(batch_years)
            options={}
            for batch_year in batch_years:
                sql4 = "SELECT DISTINCT semester FROM result_data WHERE Batch_Year = %s"
                cur.execute(sql4, batch_year)
                option = cur.fetchall()
                sems = []
                for i in option:
                    sems.append(i[0])#[1,2,3,4]
                sems=sorted(sems)
                options[batch_year[0]]=['SELECT A SEMESTER']+sems
            return options


def postresultdata(batch_year,semester,user_id):

        sql3  =  '''
            SELECT s.register_no, s.name, r.course_code, c.course_title, r.grade 
            FROM RESULT_DATA r
            JOIN CREDIT_INFO c ON r.course_code = c.course_code
            JOIN STUDENT s ON s.register_no = r.register_no
            WHERE r.semester = %s
            AND r.batch_year = %s
        '''
        # print(batch_year)
        data = (semester,batch_year)
        cur.execute(sql3,data)
        val = cur.fetchall()
       
        data_dict  =  {}

        courses = []
        # Transforming the list of tuples into a dictionary
        for row in val:
            # print(row)
            register_no = row[0]
            student_name = row[1]
            course_code = row[2]
            course_title = row[3]
            grade = row[4]

            if (register_no, student_name) not in data_dict:
                data_dict[(register_no, student_name)]  =  []
            if (course_title,course_code) not in courses:
                courses.append((course_title,course_code))

            data_dict[(register_no, student_name)].append((course_title, grade))

        data_dict = dict(sorted(data_dict.items(), key = lambda item: item[0][0]))

        # Extracting column names from the first row of the data
        column_names  = ['Register Number', 'Name']

        sql1  =  "SELECT login_id FROM login WHERE username  =  %s"
        cur.execute(sql1, (user_id,))
        login_id  =  cur.fetchone()


        sql2 = "SELECT faculty_name from faculty where login_id = %s"
        cur.execute(sql2, login_id)

        faculty_name = cur.fetchone()
            # print('batch year', batch_year)
        sql3="SELECT DISTINCT batch_year FROM faculty_batch WHERE faculty_name = %s"
        cur.execute(sql3,faculty_name)
        batch_years=cur.fetchall()
        options={}
        for batch_year in batch_years:
                sql4 = "SELECT DISTINCT semester FROM result_data WHERE Batch_Year = %s"
                cur.execute(sql4, batch_year)
                option = cur.fetchall()
                sems = []
                for i in option:
                    sems.append(i[0])#[1,2,3,4]
                sems=sorted(sems)
                options[batch_year[0]]=['SELECT A SEMESTER']+sems

        # print(options) 
        return column_names, data_dict, options, courses





def download_post_excel(batch_year, semester):

        data_dict = {}
        data = (semester,) + (batch_year,)

        sql3  =  '''
            SELECT s.register_no, s.name, r.course_code, c.course_title, r.grade 
            FROM RESULT_DATA r
            JOIN CREDIT_INFO c ON r.course_code = c.course_code
            JOIN STUDENT s ON s.register_no = r.register_no
            WHERE r.semester = %s
            AND r.batch_year = %s
        '''

        cur.execute(sql3,data)
        val = cur.fetchall()

        courses = []
        course_codes = []       # Transforming the list of tuples into a dictionary
        for row in val:
            register_no = row[0]
            student_name = row[1]
            course_code = row[2]
            course_title = row[3]
            grade  =  row[4]

            if (register_no, student_name) not in data_dict:
                data_dict[(register_no, student_name)] = []
            if course_title not in courses and course_code not in course_codes :
                courses.append(course_title)
                course_codes.append(course_code)

            data_dict[(register_no, student_name)].append((course_title, grade))
            data_dict = dict(sorted(data_dict.items(), key = lambda item: item[0][0]))

        courses = ['Register Number','Name'] + courses
        course_codes = ['',''] + course_codes
        data_list = []
        for key, value in data_dict.items():
                register_no, student_name = key
                grades  =  [grade for _, grade in value]  # Extracting grades from the list of (course_title, grade) tuples
                data_list.append([register_no, student_name] + grades)

        # print('downloading excel sheet')
        filename = str(batch_year) + '_' + str(semester)

        column_names_grades1 = ['S.No', 'Register Number', 'Name', 'O', 'A+', 'A', 'B+', 'B', 'C', 'RA', 'AB', 'WH', 'Grade Point', 'GPA', 'CGPA', 'Deviation', 'Result Status', 'Ranking']
        grade_data = display_statistics(semester,batch_year)


        #for subjectwise summary
        col=semester_data(semester,batch_year)
        subsum=[]

        for item in col:
            data = [
                item,
                tot_candid(semester,batch_year),
                Registered(item,semester,batch_year),
                Appeared(item,semester,batch_year),
                Reappear(item, semester,batch_year),
                Grade_Count('AB',item,semester,batch_year),
                Grade_Count('WH',item,semester,batch_year),
                Reappear(item, semester,batch_year) + Grade_Count('AB',item,semester,batch_year),
                Total_Grades(item, semester,batch_year),
                Grade_Count('O',item,semester,batch_year),
                Grade_Count('A+',item,semester,batch_year),
                Grade_Count('A',item,semester,batch_year),
                Grade_Count('B+',item,semester,batch_year),
                Grade_Count('B',item,semester,batch_year),
                Grade_Count('C',item,semester,batch_year),
                Pass_Percentage(item,semester,batch_year)
            ]
            subsum.append(data)

        # overall analysis        
        oa_col_names1 = ['CATEGORY', 'STRENGTH']
        oa_col_names2 = ['CATEGORY', 'STATISTICS']
        oa_col_names3 = ['GPA RANGE', 'NO. OF STUDENTS']
        oa_col_names4 = ['COURSE NO', 'NO. OF STUDENTS']

        oa_data_1 = [
            ['ALL CLEAR', no_backlogs_sem(semester,batch_year)],
            ['REAPPEAR', backlogs_sem(semester,batch_year)],
            ['ABSENT', absentee_count(semester,batch_year)],
            ['TOTAL', tot_candidates(semester,batch_year)],
            ['OVERALL CLEAR %', Overall_Pass_Percentage(semester,batch_year)]
        ]

        oa_data_2 = [
            ['MEAN GPA', Mean_GPA(semester,batch_year)],
            ['STANDARD DEVIATION', Standard_Deviation(semester,batch_year)]
        ]

        oa_data_3 = [
            ['GREATER THAN 9', GPA_count(semester,batch_year)[9]],
            ['GREATER THAN 8.5', GPA_count(semester,batch_year)[8.5]],
            ['GREATER THAN 8', GPA_count(semester,batch_year)[8]],
            ['GREATER THAN 7.5', GPA_count(semester,batch_year)[7.5]],
            ['GREATER THAN 6', GPA_count(semester,batch_year)[6]]
        ]

        oa_data_4 = [
            ['1 COURSE', Reappear_count(semester,batch_year)[1]],
            ['2 COURSES', Reappear_count(semester,batch_year)[2]],
            ['3 COURSES', Reappear_count(semester,batch_year)[3]],
            ['4 COURSES', Reappear_count(semester,batch_year)[4]],
            ['5 COURSES', Reappear_count(semester,batch_year)[5]],
            ['6 COURSES', Reappear_count(semester,batch_year)[6]],
            ['7 COURSES', Reappear_count(semester,batch_year)[7]],
            ['8 COURSES', Reappear_count(semester,batch_year)[8]]
        ]

        oa_summary = [oa_col_names1, oa_data_1,
                      oa_col_names2, oa_data_2,
                      oa_col_names3, oa_data_3,
                      oa_col_names4, oa_data_4]

        write_to_excel(filename, courses, course_codes, data_list, column_names_grades1, grade_data, subjsum_col(), subsum, oa_summary)   

def grade_analysis_colums():

    lst = ['S.No', 'Register Number', 'Name']
    lst1 = ['Grade Count']
    lst2 = ['Grade Analysis']
    lst_sub = ['O', 'A+', 'A', 'B+', 'B', 'C', 'RA', 'AB', 'WH', 'SA', 'Grade Point', 'GPA', 'CGPA', 'Deviation', 'Result Status', 'Ranking']

    return lst, lst1, lst2, lst_sub

def subjsum(semester,batch_year):
    subsum=[]
    col=semester_data(semester,batch_year)
    for item in col:
        data = [
            item,
            tot_candid(semester,batch_year),
            Registered(item,semester,batch_year),
            Appeared(item,semester,batch_year),
            Grade_Count('AB',item,semester,batch_year),
            Reappear(item, semester,batch_year),
            Grade_Count('WH',item,semester,batch_year),
            Reappear(item, semester,batch_year) + Grade_Count('AB',item,semester,batch_year),
            Total_Grades(item, semester,batch_year),
            Grade_Count('O',item,semester,batch_year),
            Grade_Count('A+',item,semester,batch_year),
            Grade_Count('A',item,semester,batch_year),
            Grade_Count('B+',item,semester,batch_year),
            Grade_Count('B',item,semester,batch_year),
            Grade_Count('C',item,semester,batch_year),
            Pass_Percentage(item,semester,batch_year)
        ]
        subsum.append(data)
    #print(subsum)
    return subsum
#subjsum(1,'2022-2026')

def subjsum_col():
    return ['COURSE CODE','TOTAL','REGISTERED','APPEARED','ABSENT','REAPPEARING','WH',
                       'REAPPEARING CANDIDATES','TOTAL WITH GRADE','O','A+','A','B+','B','C','PASS PERCENATGE']
     