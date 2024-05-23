# CONNECTING TO THE DATABASE

import mysql.connector,statistics
#from nba_analysis import tot_candidates,no_backlogs_sem

mydb = mysql.connector.connect(
        host = "localhost",
        user = "ra",
        password = "1234",
        database = "Result_analysis"
    )
cur = mydb.cursor()


# NECESSARY IMPORTS OF FUCTIONS OR MODULES

# For reading the raw data from the excel file
# from read_excel import filter_data

# column_name, column_values = filter_data()

import pandas as pd


# USER DEFINED FUNCTIONS

def Mean_GPA(sem,batch_year):
    '''
    To calculate the mean GPA for a semester's
    result summary.
    '''
    col = 'SEM' + str(sem) + '_GPA'
    avg_query = f'''SELECT AVG({col}) FROM grades
                  where batch_year="{batch_year}"'''
    cur.execute(avg_query)
    avg_gpa = cur.fetchone()[0]
    # print("Mean GPA:", avg_gpa)
    return avg_gpa

# Mean_GPA(1,'2022-2026')


def Standard_Deviation(sem,batch_year):
    '''
    To calculate the standard deviation of GPA 
    for a semester's result summary.
    '''
    
    gpa_list = []
    col = 'SEM' + str(sem) + '_GPA'
    select_query = f'''SELECT {col} FROM grades
                    where batch_year="{batch_year}"'''
    cur.execute(select_query)
    gpa_results = cur.fetchall()

    for result in gpa_results:
        gpa_value = result[0]
        if gpa_value is not None:
            gpa_list.append(gpa_value)

    std_dev = statistics.stdev(gpa_list)
    return std_dev



def no_backlogs_sem(sem,batch_year):#using sem-wise hoa
    '''This functions returns the headcount of
    the number of students without any backlogs 
    in a semester.
    '''
    sem_hoa = 'SEM'+str(sem)+'_HOA'
    select = f'''SELECT count(distinct(g.Register_No))
                FROM Grades g
                WHERE g.{sem_hoa}=0
                and g.batch_year="{batch_year}"'''
    
    cur.execute(select)
    result = cur.fetchone()[0]  # Fetch the count from the result
    return result

def tot_candidates(sem,batch_year):
    '''This functions returns the headcount of
    the total number of students who registered
    for the exam.
    '''
    grade='-'
    select = f'''SELECT COUNT(distinct(r.Register_No)) 
            FROM Result_Data r
            WHERE r.semester = {sem}
            AND r.Grade <> "{grade}"
            and r.batch_year="{batch_year}"'''
    
    cur.execute(select)
    result = cur.fetchone()[0]  # Fetch the count from the result
    return result

def Overall_Pass_Percentage(sem,batch_year):
    '''
    Returns the pass percentage
    for the given course code
    '''
    allpass = no_backlogs_sem(sem,batch_year)  
    tot = tot_candidates(sem,batch_year) 

    # Avoid division by zero error
    if tot == 0:
        # print("Error: No candidates found for the given course code.")
        return None

    pass_percent = (allpass / tot) * 100
    pass_percent = round(pass_percent, 2)

    return pass_percent



def GPA_count(semester,batch_year):
    '''This function is used to count the number of students
    who's gpa is greater than or equal to a given gpa'''

    gpas = {}
    for gpa_val in [9, 8.5, 8, 7.5, 6]:
        
        gpa_col = 'SEM'+str(semester)+'_GPA'

        gpa = f'''SELECT COUNT(*) FROM Grades WHERE {gpa_col} >= %s
                and batch_year="{batch_year}"'''
        cur.execute(gpa, (gpa_val,)) 

        res = cur.fetchone()
        mydb.commit()
        gpas[gpa_val] = res[0]
        # print(gpas)
    return gpas

def Reappear_count(semester,batch_year):
    '''This function is used to count the number of students
    with reappear count equal to a given RA count'''

    RAs = {}
    for ra_val in [1, 2, 3, 4, 5, 6, 7, 8]:

        ra_col = 'SEM'+str(semester)+'_HOA'

        ra = f'''SELECT COUNT(*) FROM grades WHERE ({ra_col} = %s)
                and batch_year="{batch_year}"'''
        cur.execute(ra, (ra_val,))

        res = cur.fetchone()
        mydb.commit()
        RAs[ra_val] = res[0]
        # print(RAs)
    return RAs

def absentee_count(semester,batch_year):
    '''This function returns the total no. of
    students who were absent for the particular
    semester examination'''

    query = f'''SELECT COUNT(DISTINCT(r.Register_No))
                FROM result_data r
                WHERE r.semester = {semester}
                AND r.Grade = "AB"
                and batch_year="{batch_year}"'''
    cur.execute(query)
    result = cur.fetchall()
    # print(result)
    return result[0][0]


def backlogs_sem(sem,batch_year):#using sem-wise hoa
    '''This functions returns the headcount of
    the number of students with backlogs 
    in any semester.
    '''
    select = f'''SELECT count(distinct(g.Register_No))
                FROM Grades g
                WHERE g.SEM{sem}_HOA!=0
                and batch_year="{batch_year}"'''
    
    cur.execute(select)
    result = cur.fetchone()[0]  # Fetch the count from the result
    return result