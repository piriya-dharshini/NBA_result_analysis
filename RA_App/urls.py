from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login, name="login"),
    path('upload/', views.upload, name="upload"),
    path('result_data/',views.result_data,name='result_data'),
    path('download_excel/',views.download_excel,name='download_excel'),
    path('grade_analysis/',views.grade_analysis,name='grade_analysis'),
    path('summary/', views.summary, name='summary'),
    path('overall_summary/', views.overall_summary, name='overall_summary'),
    path('subject_summary/', views.subject_summary, name='subject_summary'),
    path('visualize_os/', views.visualize_os, name='visualize_os'),
    path('visualize_ss/', views.visualize_ss, name='visualize_ss'),
]
