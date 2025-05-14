from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'projects'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('new-project/', views.newProject, name='new-project'),
    path('new-task/', views.newTask, name='new-task'),
    path('project-details/', views.project_details_view, name='project_details_form'),
    path('projects-edit', views.project_detail_edit, name='project_list'),
    path('projected-info/add/', views.projected_info_add, name='projected_info_add'),
    path('run-scripts/', views.run_scripts, name='run_scripts'),
    path('export-tasks/excel/', views.export_tasks_excel, name='export_tasks_excel'),
    path('export-tasks/txt/', views.export_tasks_txt, name='export_tasks_txt'),
    path('export_tasks/', views.export_tasks, name='select_project'),
    path('dual/', views.dual_view, name='dual_view'),
]