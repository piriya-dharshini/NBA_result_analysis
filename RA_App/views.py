from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from django.db import connection
from insert_values import *
from fetch import *
from summary import *
from Visualization_OS import GPA_pie
from Visualization_SS import RA_bar
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
import json

def home(request):

    return render(request, 'login.html')


def login(request):


    if request.method == "POST":

        username = request.POST['user']
        password = request.POST['pass']

        x = login1(username,password)
        request.session['user_id']=username
        # print(x)
        # print(username,password)
        if x == True:
            return redirect('/upload/upload')
    return render(request,'login.html')


def upload(request):

    if request.method == "GET":
        user_id = request.session.get('user_id', None)
        with connection.cursor() as cur:
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
            options=[]
            for batch_year in batch_years:
                # sql4 = "SELECT DISTINCT semester FROM result_data WHERE Batch_Year = %s"
                # cur.execute(sql4, batch_year)
                # option = cur.fetchall()
                # sems = []
                # for i in option:
                #     sems.append(i[0])#[1,2,3,4]

                # comp=[]
                # acc_semester=[1,2,3,4,5,6,7,8]
                # for i in acc_semester:
                #     if i not in sems:
                #         comp.append(i)
                # options[batch_year[0]]=comp #{2020-2024:[8],2021-2025:[6,7,8],2022-2026:[5,6,7,8],2023-2027:[2,3,4,5,6,7,8]}
                options.append(batch_year[0])
        return render(request, "upload.html",{'batch_semesters': options})

    if request.method == "POST":
        batchyear = request.POST['batchYear']
        status = request.POST['status']
        excel_file = request.FILES['upload']
        semester = request.POST['semester']
        with connection.cursor() as cur:
            sql4 = "SELECT DISTINCT semester FROM result_data WHERE Batch_Year = %s"
            cur.execute(sql4, (batchyear,))
            option = cur.fetchall()
        ops=[]
        for i in option:
             ops.append(i[0])
        if int(semester) in ops and status=='beforeReval':
            return render(request,"alreadyuploaded.html")
        else:
            uploadpost(batchyear, status, excel_file, semester)
            return redirect('/upload/upload')

def result_data(request):

    if request.method=="GET":

        user_id = request.session.get('user_id', None)

        options = getresultdata(user_id)
        return render(request,'result_data.html',{'batch_semesters':options})

    if request.method == "POST":
        batch_year = request.POST['batchYear']
        semester = request.POST['semester']
        user_id = request.session.get('user_id', None)
        column_names, data_dict, options, courses = postresultdata(batch_year,semester,user_id)
        return render(request, 'result_data.html', {'column_names': column_names, 'data_dict' : data_dict, 'batch_semesters' : options, 'courses' : courses,'batch':batch_year,'sem':semester})


def download_excel(request):

    if request.method=='GET':

        user_id = request.session.get('user_id', None)
        with connection.cursor() as cur:
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
            # print('get options:',options)
        return render(request,'download_excel.html', {'batch_semesters' : options})

    if request.method=='POST':
        batch_year = request.POST['batchYear']
        semester = request.POST['semester']
        download_post_excel(batch_year,semester)

        fname = str(batch_year) + "_" + str(semester) + ".xlsx"

        file = open(fname, "rb")

        response = FileResponse(file, as_attachment=True)

        response["Content-Disposition"] = f"attachment; filename = {fname}.xlsx"

        return response


def grade_analysis(request):

    from fetch import display_statistics

    class Data:

        def __init__(self, sno, regno, name, O, APlus, A, BPlus, B, C, RA, AB, WH, SA, grade_point, gpa, cgpa, deviation, status, rank):

            self.sno = sno
            self.regno = regno
            self.name = name
            self.O = O
            self.APlus = APlus
            self.A = A
            self.BPlus = BPlus
            self.B = B
            self.C = C
            self.RA = RA
            self.AB = AB
            self.WH = WH
            self.SA = SA
            self.grade_point = grade_point
            self.gpa = gpa
            self.cgpa = cgpa
            self.deviation = deviation
            self.status = status
            self.rank = rank

    col1, col2, col3, col4 = grade_analysis_colums()

    if request.method == "GET":

        user_id = request.session.get('user_id', None)
        with connection.cursor() as cur:
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
            # print('get options:',options)
        return render(request, 'grade_analysis.html', {'batch_semesters' : options})

    if request.method == "POST":

        batchYear = request.POST['batchYear']
        semester = request.POST['semester']
        user_id = request.session.get('user_id', None)
        with connection.cursor() as cur:
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


            res = display_statistics(semester,batchYear)
            data = []

            for item in res:
                data.append(Data(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10], item[11], item[12], item[13], item[14], item[15], item[16], item[17], item[18]))
            # print(res)
        return render(request, 'grade_analysis.html', {'col1' : col1, 'col2' : col2, 'col3' : col3, 'col4' : col4, "data" : data, 'batch_semesters' : options,'batch':batchYear,'sem':semester})
    
def summary(request):

    if request.method == "GET":
        return render(request, 'Summary_selection.html')
    if request.method == "POST":
        return render(request, 'Summary_selection.html')
    
def overall_summary(request):

    class Summary_attr:

        def __init__(self, gpa_9, gpa_8_5, gpa_8, gpa_7_5, gpa_6, ra_1, ra_2, ra_3, ra_4, ra_5, ra_6, ra_7, ra_8, 
                     pass_per, pass_no, arrear_no, reg_no, absent_no, mean_gpa, std_dev):
                
            self.A_9 = gpa_9
            self.A_8_5 = gpa_8_5
            self.A_8 = gpa_8
            self.A_7_5 = gpa_7_5
            self.A_6 = gpa_6
            self.RA_1 = ra_1
            self.RA_2 = ra_2
            self.RA_3 = ra_3
            self.RA_4 = ra_4
            self.RA_5 = ra_5
            self.RA_6 = ra_6
            self.RA_7 = ra_7
            self.RA_8 = ra_8
            self.Pass_per = pass_per
            self.Pass_no = pass_no
            self.Arrear_no = arrear_no
            self.Reg_no = reg_no
            self.Absent_no = absent_no
            self.Mean_gpa = mean_gpa
            self.Std_dev = std_dev

    if request.method == "GET":

        user_id = request.session.get('user_id', None)
        with connection.cursor() as cur:
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
            # print('get options:',options)
        return render(request, 'Overall_Summary.html', {'batch_semesters' : options})
    
    elif request.method == "POST":

        batchYear = request.POST['batchYear']
        semester = request.POST['semester']
        user_id = request.session.get('user_id', None)
        with connection.cursor() as cur:
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

        
        Gpas = GPA_count(semester,batchYear)
        RAs = Reappear_count(semester,batchYear)
        opp = Overall_Pass_Percentage(semester,batchYear)
        pass_no = no_backlogs_sem(semester,batchYear)
        reg_no = tot_candidates(semester,batchYear)
        absent_no = absentee_count(semester,batchYear)
        arrear_no = backlogs_sem(semester,batchYear)
        mean_gpa = Mean_GPA(semester,batchYear)
        std_dev = Standard_Deviation(semester,batchYear)
        GPA_pie(semester,batchYear) # for creating pie chart

        data = []

        data.append(Summary_attr(Gpas[9], Gpas[8.5], Gpas[8], Gpas[7.5], Gpas[6], 
                                 RAs[1], RAs[2], RAs[3], RAs[4], RAs[5], RAs[6], RAs[7], RAs[8],
                                 opp, pass_no, arrear_no, reg_no, absent_no, mean_gpa, std_dev))
        
        return render(request, 'Overall_Summary.html', {'data': data, 'batch_semesters' : options,'batch':batchYear,'sem':semester})

def subject_summary(request):

    if request.method=="GET":

        user_id = request.session.get('user_id', None)
        with connection.cursor() as cur:
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
            # print('get options:',options)
        return render(request, 'subjsum.html', {'batch_semesters' : options})

    if request.method == "POST":
        
        batchYear = request.POST['batchYear']
        semester = request.POST['semester']
        user_id = request.session.get('user_id', None)
        with connection.cursor() as cur:
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
        
        res = subjsum(semester,batchYear)
        col = subjsum_col()
        RA_bar(semester,batchYear) # for creating bar graph
        return render(request, 'subjsum.html', {'batch_semesters' : options, 'res' : res, 'col' : col,'batch':batchYear,'sem':semester})
    
def visualize_os(request):
        
    return render(request, 'Visualization_GPA.html')

def visualize_ss(request):
        
    return render(request, 'Visualization_RA.html')